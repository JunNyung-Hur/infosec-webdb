from multiprocessing import pool, cpu_count
import itertools as it
from pymongo.errors import BulkWriteError
from mongodb import init_db
import os, simplejson, time

VIRUSSIGN_PE_DIR = r'/home/seclab_db/data/virussign/pe/indexing'
VIRUSSHARE_PE_DIR = r'/home/seclab_db/data/virusshare/pe/indexing'
LABEL_DIR = r'/home/seclab_db/data/label/virussign'

def remove_virusshare_date(db):
    collection = db.raw_files
    collection.update({}, {'$unset': {'virusshare_date': 1}}, multi=True)

def insert_virussign(db):
    collection = db.raw_files
    for root, dirs, files in os.walk(VIRUSSIGN_PE_DIR):
        print(root)
        start_time = time.time()
        for file in files:
            md5 = os.path.splitext(file)[0]
            path = os.path.join(root, file)
            virussign_date = os.path.split(root)[1]
            origin_doc = collection.find_one({'md5': md5})
            if not origin_doc:
                collection.insert_one(
                    {
                        "md5": md5,
                        "path": path,
                        'virussign_date': virussign_date
                    }
                )
            else:
                if not 'virussign_date' in origin_doc:
                    collection.update_one(
                        {"_id": origin_doc['_id']},
                        {"$set":
                            {
                                'virussign_date': virussign_date
                            }
                        }
                    )
        print('finish', time.time()-start_time)


def insert_virusshare(db):
    collection = db.raw_files
    for root, dirs, files in os.walk(VIRUSSHARE_PE_DIR):
        print(root)
        start_time = time.time()
        for file in files:
            md5 = os.path.splitext(file)[0]
            path = os.path.join(root, file)
            virusshare_date = os.path.split(root)[1]
            origin_doc = collection.find_one({'md5': md5})
            if not origin_doc:
                collection.insert_one(
                    {
                        "md5": md5,
                        "path": path,
                        'virusshare_date': virusshare_date
                    }
                )
            else:
                if not 'virusshare_date' in origin_doc:
                    collection.update_one(
                        {"_id": origin_doc['_id']},
                        {"$set":
                            {
                                'virusshare_date': virusshare_date
                            }
                        }
                    )
        print('finish', time.time()-start_time)


def insert_label(db):
    collection = db.raw_files
    for root, dirs, files in os.walk(LABEL_DIR):
        print(root)
        start_time = time.time()
        for file in files:
            md5 = os.path.splitext(file)[0]
            with open(os.path.join(root, file), 'r') as f:
                label_json = simplejson.load(f)
            if not 'scans' in label_json:
                continue
            label_dict = label_json['scans']
            label_doc = dict()
            label_doc['md5'] = md5
            label_list = list()
            if 'Kaspersky' in label_dict:
                kaspersky_dict = label_dict['Kaspersky']
                kaspersky_dict['company'] = 'Kaspersky'
                label_list.append(kaspersky_dict)

            if 'BitDefender' in label_dict:
                bitdefender_dict = label_dict['BitDefender']
                bitdefender_dict['company'] = 'BitDefender'
                label_list.append(bitdefender_dict)

            if 'Symantec' in label_dict:
                symantec_dict = label_dict['Symantec']
                symantec_dict['company'] = 'Symantec'
                label_list.append(symantec_dict)
            label_doc['labels'] = label_list
            origin_doc = collection.find_one({'md5': md5})
            if not origin_doc:
                collection.insert_one(label_doc)
            else:
                collection.update_one(
                    {
                        "_id": origin_doc['_id']
                    },
                    {
                        "$set": {
                            'labels': label_doc['labels']
                        }
                    }
                )
        print('finish', time.time()-start_time)


if __name__ == '__main__':
    db = init_db()
    # insert_label(db)
    insert_virussign(db)
    insert_virusshare(db)
