from database.models import RawFile, Virussign, Virusshare, Kisa, Benign, Kaspersky, BitDefender, Symantec
from database import db_session, init_db
import os

VIRUSSIGN_PE_DIR = r'/home/seclab_db/database/virussign/pe'
VIRUSSHARE_PE_DIR = r'/home/seclab_db/database/virusshare/pe'



def insert_virussign_data():

    counter = 1
    for root, dirs, files in os.walk(VIRUSSIGN_PE_DIR):
        for file in files:
            md5 = os.path.splitext(file)[0]
            md5_exists = RawFile.query.filter_by(md5=md5).scalar() is not None
            path = os.path.join(root, file)
            collected_date = os.path.split(root)[1]
            print("{} / {} / {}".format(md5, collected_date, counter))
            if not md5_exists:
                new_md5 = RawFile(md5, path)
                db_session.add(new_md5)
            else:
                print('rawfile exist')
            virussign_data_exists = Virussign.query.filter_by(raw_file_md5=md5).scalar() is not None
            if not virussign_data_exists:
                new_virussign_data = Virussign(md5, collected_date)
                db_session.add(new_virussign_data)
            else:
                print('virussign data exist')
            db_session.commit()
            db_session.close()
            counter += 1

if __name__ == '__main__':
    init_db()
    insert_virussign_data()
