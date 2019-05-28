import pymongo
import settings
import re


def init_db():
    connection = pymongo.MongoClient(settings.MONGODB_URI)
    db = connection.seclab_db
    return db


if __name__ == '__main__':
    db = init_db()
    db.raw_file.find(
    )

    pipeline = [
        # {"$match": {"labels": {"$elemMatch": {'company': "Kaspersky", "result": {'$regex': re.compile('ransom', re.I)}}}}},
        {"$match": {"labels": {"$elemMatch": {'company': "Kaspersky", "detected": True}}}},
        {'$lookup':
            {
                'from': "label",
                'localField': "md5",
                'foreignField': "md5",
                'as': "label_doc"
            }
        },
        #{'$limit': 10},
    ]

    counter=1
    for doc in db.label.aggregate(pipeline):
        print(counter)
        counter+=1