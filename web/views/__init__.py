from web.views.index import index_blueprint

def setup_app(app):
    app.register_blueprint(index_blueprint, url_prefix='/')