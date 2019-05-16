from celery_package import celery

@celery.task()
def search_task(channel_list, start_date, end_date, label_company, label, limit, user_id):
    return True