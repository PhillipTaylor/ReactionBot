#!/usr/bin/env python
# -*- coding: utf-8


from sqlalchemy import Column, Integer, String
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
# hack? to allow using 8-bit bytestrings
engine.connect().connection.connection.text_factory = str

class Remind(Base):
    __tablename__ = 'plugin_reminder'

    id = Column(Integer, primary_key=True)
    key = Column(String(45))
    value =  Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
       return "<Reminder('%s','%s')>" % (self.key, self.value)


class DbCache(icache.ICache):
    """Cache implementation, using sqlalchemy"""
    def __init__(self):
        metadata.create_all(engine)

    def add(self, key, value):
        key = key
        value = value
        session.add(Remind(key=key, value=value))

    def get(self, key):
        key = key
        return [r.value for r in session.query(Remind).filter(Remind.key == key)]

    def drop(self, key):
        key = key
        for data in session.query(Remind).filter(Remind.key == key):
            session.delete(data)
