from multiprocessing import pool, cpu_count
import itertools as it
from pymongo.errors import BulkWriteError
from mongodb import init_db
import os, simplejson, time

VIRUSSIGN_PE_DIR = r'/home/seclab_db/database/virussign/pe/indexing'
VIRUSSHARE_PE_DIR = r'/home/seclab_db/database/virusshare/pe/indexing'
LABEL_DIR = r'/home/seclab_db/database/label/virussign'


def insert_virussign(db):
    #db.raw_files.remove({})

    collection = db.raw_files
    for root, dirs, files in os.walk(VIRUSSIGN_PE_DIR):
        print(root)
        start_time = time.time()
        raw_file_docs = list()
        for file in files:
            md5 = os.path.splitext(file)[0]
            path = os.path.join(root, file)
            virussign_collected_date = os.path.split(root)[1]
            raw_file_docs.append(
                {
                    "md5": md5,
                    "path": path,
                    'virussign_collected_date': virussign_collected_date
                }
            )
        print(len(raw_file_docs))
        if len(raw_file_docs):
            collection.insert_many(raw_file_docs)
        print('finish', time.time()-start_time)


def insert_virusshare(db):
    collection = db.raw_files
    for root, dirs, files in os.walk(VIRUSSHARE_PE_DIR):
        print(root)
        start_time = time.time()
        for file in files:
            md5 = os.path.splitext(file)[0]
            path = os.path.join(root, file)
            virusshare_collected_date = os.path.split(root)[1]
            origin_doc = collection.find_one({'md5': md5})
            if not origin_doc:
                collection.insert_one(
                    {
                        "md5": md5,
                        "path": path,
                        'virusshare_collected_date': virusshare_collected_date
                    }
                )
            else:
                if not 'virusshare_collected_date' in origin_doc:
                    collection.update_one(
                        {"_id": origin_doc['_id']},
                        {"$set":
                            {
                                'virusshare_collected_date': virusshare_collected_date
                            }
                        }
                    )
        print('finish', time.time()-start_time)

def read_label_report(root, file):
    md5 = os.path.splitext(file)[0]
    f = open(os.path.join(root, file), 'r')
    read_data = f.read()
    label_dict = simplejson.loads(read_data)
    if not 'scans' in label_dict:
        return
    label_dict = label_dict['scans']
    f.close()
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
    return label_doc


def insert_label(db):
    collection = db.labels
    for root, dirs, files in os.walk(LABEL_DIR):
        print(root)
        start_time = time.time()
        with pool.Pool(processes=cpu_count()) as mp:
            label_docs = mp.starmap(read_label_report, zip(it.repeat(root), files))
        print(len(label_docs))
        label_docs = [label_doc for label_doc in label_docs if label_doc is not None]
        if len(label_docs):
            try:
                collection.insert_many(label_docs, ordered=False)
            except BulkWriteError:
                print('except occur')
            print('finish', time.time()-start_time)


if __name__ == '__main__':
    db = init_db()
    insert_virussign(db)
    insert_virusshare(db)
