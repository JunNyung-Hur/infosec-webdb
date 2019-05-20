from flask import request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import login_required, current_user
from database import db_session
from database.models import Query
from sqlalchemy import desc
import settings, os


def setup_app(app):
    socket_io = SocketIO(app, message_queue=settings.CELERY_BROKER_URL)

    @socket_io.on('connect', namespace='/socket')
    @login_required
    def socket_connect():
        join_room(session['uid'], request.sid, namespace='/socket')
        print('connect socket: ', request.sid)

    @socket_io.on('disconnect', namespace='/socket')
    @login_required
    def socket_connect():
        leave_room(session['uid'], request.sid, namespace='/socket')
        print('disconnect socket: ', request.sid)

    @socket_io.on('search', namespace='/socket')
    @login_required
    def search(message):

        user_id = current_user.id
        last_query = db_session.query(Query).filter(Query.user_id == user_id).order_by(desc(Query.id)).first()
        if last_query and last_query.status == 0:
            emit('pending_exist')
            return False
        channel_list = message['channel']
        start_date = message['start-collected']
        end_date = message['end-collected']
        label_company = message['label-company']
        label = message['label']
        limit = message['limit']
        user_queries = db_session.query(Query).filter(Query.user_id == user_id).order_by(Query.created_at).all()
        while len(user_queries) > 9:
            db_session.delete(user_queries[0])
            db_session.commit()
            try:
                os.remove(user_queries[0].result_path)
            except Exception:
                print('Not such a query file does not exist')
            user_queries.remove(user_queries[0])
        from celery_package.tasks import search_task
        search_task.delay(channel_list, start_date, end_date, label_company, label, limit, user_id=user_id,
                          redis_url=settings.CELERY_BROKER_URL, room=session['uid'])