from mongodb import init_db


def raw_file_collection_index(db):
    raw_file_collection = db.raw_file
    raw_file_collection.create_index('md5', unique=True)
    raw_file_collection.create_index('virussign_collected_date')
    raw_file_collection.create_index('virusshare_collected_date')
    raw_file_collection.create_index([('md5',1), ('virussign_collected_date',1)])
    print(list(raw_file_collection.index_information()))

def label_collection_index(db):
    label_collection = db.label
    label_collection.create_index('md5', unique=True)
    label_collection.create_index('labels')
    label_collection.create_index('labels.company')
    label_collection.create_index('labels.detected')
    label_collection.create_index('labels.result')
    label_collection.create_index([('labels.company',1), ('labels.result',1)])
    print(list(label_collection.index_information()))


if __name__ == '__main__':
    db = init_db()
    raw_file_collection_index(db)
    label_collection_index(db)
