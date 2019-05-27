from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import settings

engine = create_engine(settings.MYSQL_URI, echo=settings.MYSQL_ECHO)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from web.database import models
    Base.metadata.create_all(engine)
    db_session.commit()
    db_session.close()
