from celery import Task
from celery_package import celery
from database.models import Virussign, Virusshare, Kisa, Kaspersky, BitDefender, Symantec, Benign, RawFile, Query
from database import session
from sqlalchemy import or_, desc
import datetime

class QueryTask(Task):

    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                    link=None, link_error=None, shadow=None, **options):
        _session = session
        _user_id = kwargs['user_id']
        _query = Query(_user_id, 0, 'test')
        _session.add(_query)
        _session.commit()

        return super(QueryTask, self).apply_async(args=args, kwargs=kwargs, task_id=task_id, producer=producer,
                                                  link=link, link_error=link_error, shadow=shadow, **options)

    def on_failure(self, exc, task_id, args, kwargs, einfo):

        _session = session
        _user_id = kwargs['user_id']
        _query = session.query(Query).filter(Query.user_id == _user_id).order_by(desc(Query.id)).first()
        _query.status = 2
        _session.commit()

    def on_success(self, retval, task_id, args, kwargs):
        _session = session
        _user_id = kwargs['user_id']
        _query = session.query(Query).filter(Query.user_id == _user_id).order_by(desc(Query.id)).first()
        _query.status = 1
        _session.commit()



@celery.task(base=QueryTask)
def search_task(channel_list, start_date, end_date, label_company, label, limit, user_id):
    channel_class_list = list()
    for channel in channel_list:
        if channel == 'virussign':
            channel_class_list.append(Virussign)
        elif channel == 'virusshare':
            channel_class_list.append(Virusshare)
        elif channel == 'kisa':
            channel_class_list.append(Kisa)

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')+datetime.timedelta(days=1)

    if label_company == 'kaspersky':
        label_company = Kaspersky
    elif label_company == 'bitdefender':
        label_company = BitDefender
    elif label_company == 'symantec':
        label_company = Symantec
    elif label_company == 'benign':
        label_company = Benign

    query = session.query(RawFile).distinct().with_entities(RawFile.path)
    query = query.filter(or_(
        channel_class.raw_file_md5==RawFile.md5 for channel_class in channel_class_list)
    )
    for channel_class in channel_class_list:
        query = query.filter(channel_class.collected_at >= start_date).filter(channel_class.collected_at < end_date)
    query = query.join(label_company)
    if not label_company == Benign:
        query = query.filter(label_company.label.contains(label))
    query = query.limit(limit)
    print(query.all())
    return True

