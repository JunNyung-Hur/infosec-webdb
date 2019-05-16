from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

table_name = 'Query'
class Query(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    status = Column(Integer, nullable=True)
    result_path = Column(String(1024), nullable=False)
    created_at = Column(DateTime, server_default=datetime.datetime.now())
    updated_at = Column(DateTime, server_default=datetime.datetime.now(), server_onupdate=datetime.datetime.now())

    def __init__(self, user_id, status, result_path):
        self.user_id = user_id
        self.status = status
        self.result_path = result_path

    def __repr__(self):
        return "<"+table_name+"('%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.id, self.user_id, self.status, self.result_path, self.created_at, self.updated_at
        )
