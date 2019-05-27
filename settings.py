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
    MONGODB Variable
'''
MONGODB_HOST = config.get('MONGODB', 'HOST')
MONGODB_PORT = config.get('MONGODB', 'PORT')
MONGODB_ID = config.get('MONGODB', 'ID')
MONGODB_PASSWORD = config.get('MONGODB', 'PASSWORD')
MONGODB_NAME = config.get('MONGODB', 'DB_NAME')
MONGODB_URI = 'mongodb://%s:%s@%s:%s' % (MONGODB_ID, MONGODB_PASSWORD, MONGODB_HOST, MONGODB_PORT)
'''
    MYSQL Variable
'''
MYSQL_HOST = config.get('MYSQL', 'HOST')
MYSQL_PORT = config.get('MYSQL', 'PORT')
MYSQL_ID = config.get('MYSQL', 'ID')
MYSQL_PASSWORD = config.get('MYSQL', 'PASSWORD')
MYSQL_NAME = config.get('MYSQL', 'DB_NAME')
MYSQL_URI = 'mysql://'+MYSQL_ID+":"+MYSQL_PASSWORD+"@"+MYSQL_HOST+'/'+MYSQL_NAME
MYSQL_ECHO = config.getboolean('MYSQL', 'ECHO')


'''
    Celery Variable
'''
BROKER_HOST = config.get('CELERY', 'BROKER_HOST')
BROKER_PORT = config.get('CELERY', 'BROKER_PORT')
CELERY_BROKER_URL = 'redis://'+BROKER_HOST+':'+BROKER_PORT
CELERY_RESULT_BACKEND = 'db+mysql://'+MYSQL_ID+':'+MYSQL_PASSWORD+'@'+MYSQL_HOST+'/'+MYSQL_NAME

'''
    Etc Variable
'''
QUERY_RESULT_PATH = os.path.join(BASE_DIR, 'query')
