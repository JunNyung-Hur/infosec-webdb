from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

table_name = 'Label'
class Label(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    raw_file_md5 = Column(String(128), ForeignKey('RawFile.md5'), nullable=False, unique=True)
    Kaspersky = Column(String(64), nullable=True)
    BitDefender = Column(String(64), nullable=False)
    Symantec = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=datetime.datetime.now().strftime("%Y-%m-%d"))
    updated_at = Column(DateTime, nullable=True)
    raw_file = relationship('RawFile', back_populates='kaspersky_label')

    def __init__(self, raw_file_md5, label):
        self.raw_file_md5 = raw_file_md5
        self.label = label

    def __repr__(self):
        return "<"+table_name+"('%s', '%s', '%s','%s', '%s')>" % (self.id, self.raw_file_md5, self.label, self.created_at, self.updated_at)
