from mongodb import init_db


def raw_files_index(db):
    collection = db.raw_files
    collection.create_index('virussign_date')
    collection.create_index('virusshare_date')
    collection.create_index([('md5',1), ('virussign_date',1)])
    collection.create_index([('md5',1), ('virusshare_date',1)])
    collection.create_index('labels')
    collection.create_index('labels.company')
    collection.create_index('labels.detected')
    collection.create_index('labels.result')
    collection.create_index([('labels.company',1), ('labels.result',1)])
    collection.create_index([('labels.company',1), ('labels.detected',1)])
    print(list(collection.index_information()))


if __name__ == '__main__':
    db = init_db()
    raw_files_index(db)