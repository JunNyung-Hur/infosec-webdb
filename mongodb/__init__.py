import pymongo
import settings


def init_db():
    connection = pymongo.MongoClient(settings.MONGODB_URI)
    db = connection.seclab_db
    return db

def find_docs_by_md5_list(db, md5_list):
    collection = db.raw_files
    docs = collection.find({'md5': {'$in': md5_list}})
    return docs


if __name__ == '__main__':
    db = init_db()
    md5_list = ['fa0f33913d9f8f9c703957b978234210', 'f901bf0464c8ff868eb2d603932e04cb', 'f42ef58d30a49471c74495817799ae2b']
    docs = find_docs_by_md5_list(db, md5_list)
    for doc in docs:
        print(doc)
