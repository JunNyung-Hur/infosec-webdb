from flask_login import LoginManager
from database.models import User
from web.auth.views import auth_blueprint

def setup_app(app):

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).one()
    app.register_blueprint(auth_blueprint, url_prefix='/auth')