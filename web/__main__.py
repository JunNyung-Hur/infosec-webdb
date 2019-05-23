import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from flask import Flask
from flask_registry import Registry, ExtensionRegistry
from database import init_db
import settings

def create_app():
    app = Flask(
        settings.APP_NAME,
        template_folder=os.path.join(settings.WEB_DIR,'templates'),
        static_folder=os.path.join(settings.WEB_DIR, 'static')
    )

    app.config.update(
        DEBUG=True,
        SECRET_KEY='qwe123!@3',
        EXTENSIONS=['web.views.socket', 'web.views', 'web.auth'],
    )

    registry = Registry(app=app)
    registry['packages'] = ExtensionRegistry(app=app)
    init_db()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=settings.WEB_HOST, port=settings.WEB_PORT)