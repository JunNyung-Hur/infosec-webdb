from flask import Flask
from flask_registry import Registry, ExtensionRegistry
from flask_session import Session
import database
import settings

def create_app():
    app = Flask(settings.APP_NAME)
    app.config.update(
        DEBUG=True,
        SECRET_KEY='qwe123!@3',
        EXTENSIONS=['web.views.socket', 'web.views', 'web.auth'],
        SESSION_TYPE='filesystem'
    )
    registry = Registry(app=app)
    registry['packages'] = ExtensionRegistry(app=app)
    Session(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=settings.WEB_HOST, port=settings.WEB_PORT)