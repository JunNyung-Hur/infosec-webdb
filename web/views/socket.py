from flask import session, request
from flask_socketio import SocketIO, emit
from flask_login import login_required
import uuid, settings

def setup_app(app):
    socket_io = SocketIO(app, manage_session=False, message_queue=settings.CELERY_BROKER_URL)

    @socket_io.on('connect', namespace='/socket/queries')
    @login_required
    def queries_connect():
        socket_user_id = str(uuid.uuid4())

        session['sid'] = request.sid
        session['namespace'] = request.namespace
        emit('ready')

    @socket_io.on('response', namespace='/socket')
    def queries_test():
        print('test')