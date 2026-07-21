
def init_app(app):
    from wtforms import FieldList

    def get_field_list_data_template(field_list):
        if not isinstance(field_list, FieldList):
            return None
        field_list.append_entry()
        data = field_list.pop_entry()
        return data

    app.jinja_env.filters['mirc_field_template'] = get_field_list_data_template

    def abbrev(text, length=75):
        if not text:
            return ''

        w = text.split()
        w.reverse()
        short = ''
        while len(short) < length and len(w):
            short += ' ' + w.pop()
        if len(w):
            short += ' ...'
        return short.strip()

    app.jinja_env.filters['abbrev'] = abbrev

    from .scenarios.routes import mirc_scenario
    app.register_blueprint(mirc_scenario)

    from .scenarios.api import mirc_scenario_api
    app.register_blueprint(mirc_scenario_api)

    from .simulations.api import mirc_simulation_api
    app.register_blueprint(mirc_simulation_api)
