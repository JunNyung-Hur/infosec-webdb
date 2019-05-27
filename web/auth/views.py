from flask import request, flash, abort, redirect, render_template, url_for, Blueprint, Response, session
from flask_login import login_user, current_user, logout_user, login_required
from web.database.models import User
from web.database import db_session
from flask_socketio import close_room
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).all()
        if not len(user):
            return Response('login failed', status=400)
        user = user[0]

        if not user.check_password(password):
            return Response('login failed', status=400)
        login_user(user)
        session['uid'] = str(user.username)

        user.authenticated = True
        db_session.commit()
        db_session.close()

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
    db_session.close()
    logout_user()
    close_room(session['uid'], '/search')
    del session['uid']
    return redirect(url_for('index.index'))