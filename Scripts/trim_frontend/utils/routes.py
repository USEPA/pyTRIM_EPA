
def init_routes(app):
    from ..base.routes import base
    from ..errors.handlers import errors
    from ..file_io.routes import file_api
    from ..external_API.routes import external_api_soil, external_api_r
    from ..parcels.routes import parcels_api
    from ..scenarios.routes import scenario, scenario_api

    app.register_blueprint(base)
    app.register_blueprint(errors)
    app.register_blueprint(file_api)
    app.register_blueprint(scenario)
    app.register_blueprint(scenario_api)
    app.register_blueprint(parcels_api)
    app.register_blueprint(external_api_soil)
