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
session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = Base.metadata

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
        remind = Remind(key=key, value=value)
        session.add(remind)

    def get(self, key):
        return [data for data in session.query.filter(Remind.key == key)]

    def drop(self, key):
        for data in self.get(key):
            session.delete(data)
