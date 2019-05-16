from flask import Flask
from web import auth, views
import database
import settings

def create_app():
    app = Flask(settings.APP_NAME)
    app.config.update(
        DEBUG=True,
        SECRET_KEY='qwe123!@3'
    )
    return app


if __name__ == "__main__":
    app = create_app()
    auth.init_auth(app)
    views.init_views(app)
    app.run(host=settings.WEB_HOST, port=settings.WEB_PORT)