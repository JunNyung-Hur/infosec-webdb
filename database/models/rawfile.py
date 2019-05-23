from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

table_name = 'RawFile'
class RawFile(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    md5 = Column(String(128), nullable=False, unique=True)
    path = Column(String(1024), nullable=False)
    created_at = Column(DateTime, nullable=False)
    bitdefender_label = relationship('BitDefender', back_populates='raw_file')
    kaspersky_label = relationship('Kaspersky', back_populates='raw_file')
    symantec_label = relationship('Symantec', back_populates='raw_file')
    kisa = relationship('Kisa', back_populates='raw_file')
    virussign = relationship('Virussign', back_populates='raw_file')
    virusshare = relationship('Virusshare', back_populates='raw_file')
    benign = relationship('Benign', back_populates='raw_file')

    def __init__(self, md5, path, created_at):
        self.md5 = md5
        self.path = path
        self.created_at = created_at

    def __repr__(self):
        return "<"+table_name+"('%s', '%s', '%s', '%s')>" % (self.id, self.md5, self.path, self.created_at)
