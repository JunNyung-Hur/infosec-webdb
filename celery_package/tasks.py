from celery import Task
from celery_package import celery
from database import db_session
from database.models import Virussign, Virusshare, Kisa, Kaspersky, BitDefender, Symantec, Benign, RawFile, Query
from sqlalchemy import or_, desc
from flask_socketio import SocketIO
import datetime, settings, os


class QueryTask(Task):
    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                    link=None, link_error=None, shadow=None, **options):
        return super(QueryTask, self).apply_async(args=args, kwargs=kwargs, task_id=task_id, producer=producer,
                                                  link=link, link_error=link_error, shadow=shadow, **options)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        _user_id = kwargs['user_id']
        _query = Query.query.filter(Query.user_id == _user_id).order_by(desc(Query.id)).first()
        _query.status = 2
        db_session.commit()
        db_session.close()
        task_socket_io = SocketIO(message_queue=kwargs['redis_url'])
        task_socket_io.emit('query_failed', namespace='/socket', room=kwargs['room'])

    def on_success(self, retval, task_id, args, kwargs):
        _user_id = kwargs['user_id']
        _query = Query.query.filter(Query.user_id == _user_id).order_by(desc(Query.id)).first()
        _query.status = 1
        db_session.commit()
        db_session.close()
        task_socket_io = SocketIO(message_queue=kwargs['redis_url'])
        task_socket_io.emit('query_success', namespace='/socket', room=kwargs['room'])


@celery.task(base=QueryTask)
def search_task(file_type, channel_list, date_range, vaccine_company, label, limit, user_id, redis_url, room):
    new_query = Query(user_id, 0, 'None')
    db_session.add(new_query)
    db_session.commit()
    result_path = os.path.join(settings.QUERY_RESULT_PATH, str(user_id)+'_'+str(new_query.id)+'.txt')
    new_query.result_path = result_path
    db_session.commit()

    task_socket_io = SocketIO(message_queue=redis_url, logger=True,  engineio_logger=True)
    task_socket_io.emit('query_start', namespace='/socket', room=room)

    channel_class_list = list()
    if type(channel_list) == str:
        channel_list = [channel_list]

    for channel in channel_list:
        if channel == 'virussign':
            channel_class_list.append(Virussign)
        elif channel == 'virusshare':
            channel_class_list.append(Virusshare)
        elif channel == 'kisa':
            channel_class_list.append(Kisa)
        elif channel == 'benign-crawling':
            channel_class_list.append(Benign)

    query = RawFile.query.distinct().with_entities(RawFile.path)
    if len(channel_class_list) == 1:
        query = query.filter(channel_class_list[0].raw_file_md5 == RawFile.md5)
    else:
        query = query.filter(or_(
            channel_class.raw_file_md5 == RawFile.md5 for channel_class in channel_class_list)
        )

    if file_type == 'malware':
        if vaccine_company == 'kaspersky':
            vaccine_company = Kaspersky
        elif vaccine_company == 'bitdefender':
            vaccine_company = BitDefender
        elif vaccine_company == 'symantec':
            vaccine_company = Symantec

        query = query.join(vaccine_company)
        query = query.filter(vaccine_company.label.contains(label))

    elif file_type == 'benign':
        subquery1 = Kaspersky.query.distinct().with_entities(Kaspersky.raw_file_md5)
        subquery2 = BitDefender.query.distinct().with_entities(BitDefender.raw_file_md5)
        subquery3 = Symantec.query.distinct().with_entities(Symantec.raw_file_md5)
        query = query.filter(~RawFile.md5.in_(subquery1)).filter(~RawFile.md5.in_(subquery2)).filter(~RawFile.md5.in_(subquery3))


    if date_range:
        start_date = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(date_range[1], '%Y-%m-%d')+datetime.timedelta(days=1)

        for channel_class in channel_class_list:
            query = query.filter(channel_class.collected_at >= start_date).filter(channel_class.collected_at < end_date)

    if limit:
        query = query.limit(limit)
    query_results = query.all()
    db_session.close()

    path_list = list()
    for query_result in query_results:
        path_list.append(query_result[0])

    write_str = str()
    if len(path_list):
        for path in path_list[:-1]:
            write_str += path+'\n'
        write_str += path_list[-1]

    with open(os.path.join(settings.QUERY_RESULT_PATH, result_path), 'w') as f:
        f.write(write_str)

    return True

