import os, configparser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

def get_config():
    default_config_file = os.path.join(CONFIG_DIR, 'config.defaults.ini')

    config_list = list()
    for root, dirs, files in os.walk(CONFIG_DIR):
        for file_name in files:
            config_list.append(os.path.join(root, file_name))

    config_list.insert(0, config_list.pop(config_list.index(default_config_file)))
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(config_list)
    return config


config = get_config()

'''
    Web Variable
'''
APP_NAME = config.get('WEB', 'APP_NAME')
WEB_HOST = config.get('WEB', 'HOST')
WEB_PORT = config.get('WEB', 'PORT')

'''
    DB Variable
'''
DB_HOST = config.get('DATABASE', 'HOST')
DB_PORT = config.get('DATABASE', 'PORT')
DB_ID = config.get('DATABASE', 'ID')
DB_PASSWORD = config.get('DATABASE', 'PASSWORD')
DB_NAME = config.get('DATABASE', 'DB_NAME')
DB_URI = 'mysql://'+DB_ID+":"+DB_PASSWORD+"@"+DB_HOST+'/'+DB_NAME

'''
    Celery Variable
'''
BROKER_HOST = config.get('CELERY', 'BROKER_HOST')
BROKER_PORT = config.get('CELERY', 'BROKER_PORT')
CELERY_BROKER_URL = 'redis://'+BROKER_HOST+':'+BROKER_PORT
CELERY_RESULT_BACKEND = 'db+mysql://'+DB_ID+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_NAME

