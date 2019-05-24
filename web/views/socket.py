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
        if last_query and (last_query.status == 0 or last_query.status == 1):
            emit('pending_exist')
            db_session.close()
            return False

        new_query = Query(user_id, 0, 'None')
        db_session.add(new_query)
        db_session.commit()
        socket_io.emit('query_start', namespace='/socket', room=request.sid)
        new_query_id = new_query.id

        result_path = os.path.join(settings.QUERY_RESULT_PATH, str(user_id) + '_' + str(new_query_id) + '.txt')
        new_query.result_path = result_path
        db_session.commit()

        file_type = message['type']
        channel_list = message['channel']

        date_range = None
        if 'start-collected' in message and 'end-collected' in message:
            date_range = (message['start-collected'], message['end-collected'])
        vaccine_company = message['vaccine-company'] if 'vaccine-company' in message else None
        label = message['label'] if 'label' in message else None
        limit = message['limit'] if 'limit' in message else None
        user_queries = db_session.query(Query).filter(Query.user_id == user_id).order_by(Query.created_at).all()
        while len(user_queries) > 10:
            db_session.delete(user_queries[0])
            db_session.commit()
            try:
                os.remove(user_queries[0].result_path)
            except FileNotFoundError:
                print('Not such a query file does not exist')
            user_queries.remove(user_queries[0])
        db_session.close()

        from celery_package.tasks import search_task
        search_task.delay(
            file_type, channel_list, date_range, vaccine_company, label, limit, result_path,
            query_id=new_query_id, redis_url=settings.CELERY_BROKER_URL, room=session['uid']
        )