import json
import os
from collections import OrderedDict
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, StringField, FloatField, IntegerField, \
    FormField, FieldList, SelectField, SelectMultipleField
from wtforms.fields import DateField, DateTimeLocalField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea, ListWidget, CheckboxInput
from markupsafe import Markup
from wtforms.widgets.core import html_params
from wtforms.widgets import NumberInput


root = os.path.dirname(os.path.abspath(__file__))
forms = os.path.abspath(os.path.join(root, '../static/forms'))


def assemble_json_form(path):
    src = path
    if not os.path.abspath(src) == src:
        src = os.path.join(forms, src)

    # Try reading in the JSON data
    data = None
    try:
        if os.path.isfile(src):
            with open(src, mode='r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            print(src)
    except Exception:
        return None

    parent_src = data.get('inherits', None)
    if parent_src:
        child = data
        parent = assemble_json_form(parent_src)
        data = {**parent}
        data['title'] = child['title']

        parent_fields = {x['id']: x for x in parent['fields']}
        child_fields = {x['id']: x for x in child['fields']}

        for i in child_fields.keys():
            if i in parent_fields:
                child_fields[i] = {**parent_fields[i], **child_fields[i]}

        merged = {**parent_fields, **child_fields}
        data['fields'] = list(merged.values())

    def load_child_form(field):
        form_def = field['form_definition']
        child = assemble_json_form(form_def)
        field['form_definition'] = child

    for field in data['fields']:
        if field['data_type'] == 'form':
            load_child_form(field)

        elif field['data_type'] == 'field_list':
            if field['field']['data_type'] == 'form':
                load_child_form(field['field'])

    return data


def json_form(src):
    def decorator(cls):
        data = assemble_json_form(src)

        if not data:
            return cls

        DynamicJsonForm = create_dynamic_form_from_json(data, cls)

        return DynamicJsonForm
    return decorator


def create_dynamic_form_from_json(form_def, cls):
    class DynamicJsonForm(cls):
        pass

    # Set form title
    setattr(DynamicJsonForm, 'title', form_def['title'])

    # Add fields to dynamic form
    for field_def in form_def['fields']:
        field = create_dynamic_field_from_json(field_def)
        setattr(DynamicJsonForm, field_def['id'], field)

    return DynamicJsonForm


def create_dynamic_field_from_json(field_def):
    # Default class and properties
    field_cls = StringField
    field_props = {
        'validators': [],
        'render_kw': {}
    }

    # Determine if different field class/widget is needed
    data_type = field_def['data_type']

    widget = field_def.get('widget', None)
    widget_props = {}
    min_val = field_def.get('min', None)
    max_val = field_def.get('max', None)
    step = field_def.get('step', None)
    if min_val is not None:
        widget_props['min'] = min_val
    if max_val is not None:
        widget_props['max'] = max_val
    if step is not None:
        widget_props['step'] = step

    # First check for special widgets
    # that overrule everything else
    if widget == 'select' or data_type == 'select' \
            or widget == 'dropdown' or data_type == 'dropdown':
        field_cls = SelectField
        choices = field_def['choices']
        updated_choices = []
        for c in choices:
            if len(c) == 2:
                updated_choices.append((c[0], c[1]))
            else:
                updated_choices.append((c, c))
        field_props['choices'] = updated_choices

    elif widget == 'textarea':
        field_props['widget'] = TextArea()

    # Then, if applicable check the datatype
    elif data_type == 'bit' or data_type == 'bitwise':
        field_cls = BooleanField

    elif data_type == 'boolean' or data_type == 'bool':
        field_cls = BooleanField

    elif data_type == 'int' or data_type == 'integer':
        field_cls = IntegerField
        field_props['widget'] = NumberInput(**widget_props)
        widget_props.pop('step', None)
        field_props['validators'].append(
            NumberRange(**widget_props)
        )

    elif data_type == 'float' or data_type == 'number':
        field_cls = FloatField
        field_props['widget'] = NumberInput(**widget_props)
        widget_props.pop('step', None)
        field_props['validators'].append(
            NumberRange(**widget_props)
        )

    elif data_type == 'date':
        field_cls = DateField

    elif data_type == 'datetime':
        field_cls = DateTimeLocalField

    elif data_type == 'file':
        field_cls = FileField

    elif data_type == 'form':
        field_cls = FormField
        form_def = field_def['form_definition']
        subform = create_dynamic_form_from_json(form_def, FlaskForm)
        field_props['form_class'] = subform
        sep = field_def.get('separator', None)
        if sep is not None:
            field_props['separator'] = sep

    elif data_type == 'field_list':
        field_cls = FieldList
        subfield_def = field_def['field']
        subfield = create_dynamic_field_from_json(subfield_def)
        field_props['unbound_field'] = subfield
        mins = field_def.get('min_entries', None)
        if mins is not None:
            field_props['min_entries'] = mins
        maxs = field_def.get('max_entries', None)
        if maxs is not None:
            field_props['max_entries'] = maxs

    # Now that we've gotten the basic field class,
    # pull out any additional field properties

    # Field label
    field_props['label'] = field_def['label']

    # Field data formatting
    f = field_def.get('format', None)
    if f:
        field_props['format'] = f

    # Field default data
    default = field_def.get('default', None)
    if default is not None:
        if data_type == 'date':
            default = datetime.strptime(default, f).date()
        if data_type == 'datetime':
            default = datetime.strptime(default, f)
        field_props['default'] = default

    # Field validation
    req = field_def.get('required', False)
    if req:
        if data_type == 'file':
            field_props['validators'].append(FileRequired())
        else:
            field_props['validators'].append(DataRequired())

    # Field description text
    d = field_def.get('description', '')
    if d:
        field_props['description'] = d

    # Field help text
    h = field_def.get('help', '')
    if h:
        field_props['help_text'] = h

    # Should field be auto-disabled?
    dis = field_def.get('disabled', False)
    ro = field_def.get('readonly', False)
    if dis or ro:
        field_props['render_kw']['disabled'] = 'disabled'

    # Generate field
    field = field_cls(**field_props)

    return field


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class InlineButtonWidget(object):
    """
    Render a basic ``<button>`` field.
    """
    html_params = staticmethod(html_params)
    html = '<button %s>%s</button>'
    input_type = 'submit'

    def __call__(self, field, **kwargs):
        kwargs['name'] = field.name
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        # return HTMLString(
        #     self.html % (self.html_params(**kwargs), field.label.text)
        # )
        return Markup(
             self.html % (self.html_params(**kwargs), field.label.text)
        )

class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.
    This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()


class OrderableForm:
    field_order = None

    def __iter__(self):
        if self.field_order:
            if '*' not in self.field_order:
                self.field_order.append('*')

            temp_fields = []
            for name in self.field_order:
                if name == '*':
                    temp_fields.extend([(k, v) for k, v in self._fields.items()
                                        if k not in self.field_order])
                else:
                    temp_fields.append([(k, v) for k, v in self._fields.items()
                                        if k == name][0])

            self._fields = OrderedDict(f for f in temp_fields)

        return super(FlaskForm, self).__iter__()
