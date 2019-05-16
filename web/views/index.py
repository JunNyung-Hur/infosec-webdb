from flask import request, flash, abort, redirect, render_template, url_for, Blueprint, Response
from flask_login import current_user, login_required
from celery_package.views import search_task

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('/index.html')

@index_blueprint.route('/search', methods=['POST'])
@login_required
def search():

    channel_list = request.form.getlist('channel')
    start_date = request.form.get('start-collected')
    end_date = request.form.get('end-collected')
    label_company = request.form.get('label-company')
    label = request.form.get('label')
    limit = request.form.get('limit')

    search_task(channel_list, start_date, end_date, label_company, label, limit, current_user.id)
    return Response('', status=200)