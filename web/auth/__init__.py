from flask_login import LoginManager
from database.models import User
from database import session
from web.auth.views import auth_blueprint

def init_auth(app):

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return session.query(User).filter(User.id == user_id).one()
    app.register_blueprint(auth_blueprint, url_prefix='/auth')