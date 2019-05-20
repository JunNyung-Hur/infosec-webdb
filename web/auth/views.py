from flask import request, flash, abort, redirect, render_template, url_for, Blueprint, Response
from flask_login import login_user, current_user, logout_user, login_required
from database.models import User
from database import db_session

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if request.method == 'POST':
        # Login and validate the user.
        # user should be an instance of your `User` class
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).all()
        if not len(user):
            return Response('login failed', status=400)
        user = user[0]
        if not user.check_password(password):
            return Response('login failed', status=400)
        login_user(user)
        user.authenticated = True
        db_session.commit()

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        #if not is_safe_url(next):
        #    return abort(400)

        return Response(next or url_for('index.index'), status=200)
    return render_template('/auth/login.html')

@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db_session.commit()
    logout_user()
    return redirect(url_for('index.index'))