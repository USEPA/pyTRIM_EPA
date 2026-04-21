
def init_app(app):
    from wtforms import FieldList

    def get_field_list_data_template(field_list):
        if not isinstance(field_list, FieldList):
            return None
        field_list.append_entry()
        data = field_list.pop_entry()
        return data

    app.jinja_env.filters['mirc_field_template'] = get_field_list_data_template
