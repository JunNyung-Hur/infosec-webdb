from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

table_name = 'Virusshare'
class Virusshare(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    raw_file_md5 = Column(String(128), ForeignKey('RawFile.md5'), nullable=False, unique=True)
    collected_at = Column(DateTime, nullable=False)
    raw_file = relationship('RawFile', back_populates='virusshare')

    def __init__(self, raw_file_md5, collected_at):
        self.raw_file_md5 = raw_file_md5
        self.collected_at = collected_at

    def __repr__(self):
        return "<"+table_name+"('%s', '%s', '%s')>" % (self.id, self.raw_file_md5, self.collected_at)
