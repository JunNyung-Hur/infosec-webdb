from flask import request, flash, abort, redirect, render_template, url_for, Blueprint, Response
from flask_login import current_user, login_required
from sqlalchemy import desc
from database import session
from database.models import Query

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('/index.html')

@index_blueprint.route('/search', methods=['POST'])
@login_required
def search():
    user_id = current_user.id
    last_query = session.query(Query).filter(Query.user_id == user_id).order_by(desc(Query.id)).first()
    if last_query.status == 0:
        return Response('last query is running', status=400)
    channel_list = request.form.getlist('channel')
    start_date = request.form.get('start-collected')
    end_date = request.form.get('end-collected')
    label_company = request.form.get('label-company')
    label = request.form.get('label')
    limit = request.form.get('limit')

    from celery_package.tasks import search_task
    search_task.delay(channel_list, start_date, end_date, label_company, label, limit, user_id=user_id)
    return Response('', status=200)