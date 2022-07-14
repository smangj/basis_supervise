# coding: utf-8
# Author: smangj
from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, scoped_session

DB_path = r'./data/supervise.db'
project_engine = sa.create_engine(r'sqlite:///' + DB_path)
DBSession = sessionmaker(bind=project_engine)
Session = scoped_session(DBSession)


@contextmanager
def session_scope():

    try:
        yield Session
        Session.commit()
    except Exception as e:
        Session.rollback()
        raise e
    finally:
        Session.remove()


