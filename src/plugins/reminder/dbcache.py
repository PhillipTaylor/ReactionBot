#!/usr/bin/env python
# -*- coding: utf-8


from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import icache
import settings

"""
Cache implementation using SqlAlchemy
"""


engine = settings.DATABASE_ENGINE
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
metadata = Base.metadata

class Remind(Base):
    __tablename__ = 'plugin_reminder'

    id = Column(Integer, primary_key=True)
    key = Column(Unicode(45))
    value =  Column(Unicode)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
       return u"<Reminder('%s','%s')>" % (self.key, self.value)


class DbCache(icache.ICache):
    """Cache implementation, using sqlalchemy"""
    def __init__(self):
        metadata.create_all(engine)

    def add(self, key, value):
        key = key.decode('utf-8')
        value = value.decode('utf-8')
        session.add(Remind(key=key, value=value))

    def get(self, key):
        key = key.decode('utf-8')
        return [r.value for r in session.query(Remind).filter(Remind.key == key)]

    def drop(self, key):
        key = key.decode('utf-8')
        data = session.query(Remind).filter(Remind.key == key)
        session.delete(data)
