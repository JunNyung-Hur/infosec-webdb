from flask import request, flash, abort, redirect, render_template, url_for, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from database import session, User

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('/index.html')