from multiprocessing import pool, cpu_count
import itertools as it
import os, simplejson, time, json

VIRUSSIGN_PE_DIR = r'/home/seclab_db/data/virussign/pe/indexing'
VIRUSSHARE_PE_DIR = r'/home/seclab_db/data/virusshare/pe/indexing'
LABEL_DIR = r'/home/seclab_db/data/label/virussign'
RAW_FILES_DIR = r'/home/seclab_db/database/raw_files'


def insert_virussign_info(root, file, raw_files_dir):
    md5 = os.path.splitext(file)[0]
    path = os.path.join(root, file)
    virussign_date = os.path.split(root)[1]
    doc_path = os.path.join(raw_files_dir, md5 + '.json')
    doc_exist = os.path.isfile(doc_path)
    if doc_exist:
        with open(doc_path, 'r') as f:
            doc = json.load(f)
        if 'path' not in doc:
            doc['path'] = path
        if 'virussign_date' not in doc:
            doc['virussign_date'] = virussign_date
    else:
        doc = {
            "md5": md5,
            "path": path,
            "virussign_date": virussign_date
        }
    with open(doc_path, 'w') as f:
        json.dump(doc, f)


def insert_virusshare_info(root, file, raw_files_dir):
    md5 = os.path.splitext(file)[0]
    path = os.path.join(root, file)
    virusshare_date = os.path.split(root)[1]
    doc_path = os.path.join(raw_files_dir, md5 + '.json')
    doc_exist = os.path.isfile(doc_path)
    if doc_exist:
        with open(doc_path, 'r') as f:
            doc = json.load(f)
        if 'path' not in doc:
            doc['path'] = path
        if 'virusshare_date' not in doc:
            doc['virusshare_date'] = virusshare_date
    else:
        doc = {
            "md5": md5,
            "path": path,
            "virushare_date": virusshare_date
        }
    with open(doc_path, 'w') as f:
        json.dump(doc, f)


def insert_label_info(root, file, raw_files_dir):
    md5 = os.path.splitext(file)[0]
    doc_path = os.path.join(raw_files_dir, md5 + '.json')
    doc_exist = os.path.isfile(doc_path)
    with open(os.path.join(root, file), 'r') as f:
        label_dict = json.load(f)
    if 'scans' not in label_dict:
        return
    label_dict = label_dict['scans']

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

    if doc_exist:
        with open(doc_path, 'r') as f:
            doc = json.load(f)
        doc['labels'] = label_list

    else:
        doc = {
            'md5': md5,
            'labels': label_list
        }

    with open(doc_path, 'w') as f:
        json.dump(doc, f)


def make_raw_files_docs():
    for file in os.listdir(RAW_FILES_DIR):
        os.remove(os.path.join(RAW_FILES_DIR, file))

    for root, dirs, files in os.walk(VIRUSSIGN_PE_DIR):
        print(root)
        start_time = time.time()
        with pool.Pool(processes=100) as mp:
            mp.starmap(insert_virussign_info, zip(it.repeat(root), files, it.repeat(RAW_FILES_DIR)))
        print('finish', time.time()-start_time)

    for root, dirs, files in os.walk(VIRUSSHARE_PE_DIR):
        print(root)
        start_time = time.time()
        with pool.Pool(processes=cpu_count()) as mp:
            mp.starmap(insert_virusshare_info, zip(it.repeat(root), files, it.repeat(RAW_FILES_DIR)))
        print('finish', time.time()-start_time)

    for root, dirs, files in os.walk(LABEL_DIR):
        print(root)
        start_time = time.time()
        with pool.Pool(processes=cpu_count()) as mp:
            mp.starmap(insert_label_info, zip(it.repeat(root), files, it.repeat(RAW_FILES_DIR)))
        print('finish', time.time() - start_time)


if __name__ == '__main__':
    make_raw_files_docs()