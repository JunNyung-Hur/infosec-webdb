from flask import request, render_template, url_for, Blueprint, Response, session
from flask_login import current_user, login_required
from sqlalchemy import desc
from database import session as db_session
from database.models import Query
import json, datetime, settings

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('/index.html')


@index_blueprint.route('/search', methods=['POST'])
@login_required
def search():
    user_id = current_user.id
    last_query = db_session.query(Query).filter(Query.user_id == user_id).order_by(desc(Query.id)).first()
    if last_query and last_query.status == 0:
        return Response('last query is running', status=400)
    channel_list = request.form.getlist('channel')
    start_date = request.form.get('start-collected')
    end_date = request.form.get('end-collected')
    label_company = request.form.get('label-company')
    label = request.form.get('label')
    limit = request.form.get('limit')
    result_path = str(user_id)+'_'+str(int(datetime.datetime.now().timestamp()))+'.txt'
    user_queries = db_session.query(Query).filter(Query.user_id == user_id).order_by(Query.created_at).all()
    while len(user_queries) > 9:
        db_session.delete(user_queries[0])
        user_queries.pop(0)
    db_session.commit()

    sid = session['sid']
    namespace = session['namespace']
    from flask_socketio import join_room
    join_room(sid, sid, namespace)
    from celery_package.tasks import search_task
    search_task.delay(channel_list, start_date, end_date, label_company, label, limit, user_id=user_id, result_path=result_path, url=settings.CELERY_BROKER_URL, sid=sid, namespace=namespace)
    return Response('ok', status=200)


@index_blueprint.route('/queries', methods=['GET'])
@login_required
def get_queries():
    user_id = current_user.id
    user_queries = db_session.query(Query).filter(Query.user_id == user_id).order_by(Query.created_at).all()
    response_dict = list()
    for user_query in user_queries:
        response_dict.append({
            'query_id': user_query.id,
            'query_status': user_query.status,
            'query_created_at': str(user_query.created_at)
        })
    return Response(json.dumps(response_dict), status=200)
