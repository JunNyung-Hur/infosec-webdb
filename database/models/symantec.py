from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

table_name = 'Symantec'
class Symantec(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    raw_file_md5 = Column(String(128), ForeignKey('RawFile.md5'), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    raw_file = relationship('RawFile', back_populates='symantec_label')

    def __init__(self, raw_file_md5, created_at):
        self.raw_file_md5 = raw_file_md5
        self.created_at = created_at

    def __repr__(self):
        return "<"+table_name+"('%s', '%s', '%s', '%s')>" % (self.id, self.raw_file_md5, self.created_at, self.updated_at)
