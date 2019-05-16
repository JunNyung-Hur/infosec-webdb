from web.views.index import index_blueprint

def init_views(app):
    app.register_blueprint(index_blueprint, url_prefix='/')