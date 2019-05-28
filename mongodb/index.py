from mongodb import init_db


def raw_files_index(db):
    collection = db.raw_files
    collection.create_index('virussign_collected_date')
    collection.create_index('virusshare_collected_date')
    collection.create_index([('md5',1), ('virussign_collected_date',1)])
    print(list(collection.index_information()))

def labels_index(db):
    collection = db.labels
    collection.create_index('labels')
    collection.create_index('labels.company')
    collection.create_index('labsels.detected')
    collection.create_index('labels.result')
    collection.create_index([('labels.company',1), ('labels.result',1)])
    print(list(collection.index_information()))


if __name__ == '__main__':
    db = init_db()
    raw_files_index(db)
    labels_index(db)
