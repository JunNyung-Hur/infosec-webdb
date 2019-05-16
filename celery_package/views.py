from celery_package import celery
from database.models import Virussign, Virusshare, Kisa, Kaspersky, BitDefender, Symantec, Benign, RawFile
from database import session
from sqlalchemy import or_
from sqlalchemy.orm import load_only
import datetime

@celery.task()
def search_task(channel_list, start_date, end_date, label_company, label, limit, user_id):
    channel_class_list = list()
    for channel in channel_list:
        if channel == 'virussign':
            channel_class_list.append(Virussign)
        elif channel == 'virusshare':
            channel_class_list.append(Virusshare)
        elif channel == 'kisa':
            channel_class_list.append(Kisa)

    print(start_date)
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
    result = query.all()
    print(result)
    return True