from app import db
from sqlalchemy import Column, String, Integer, DateTime, Boolean

class Ioc(db.Model):
    __tablename__ = 'iocs'

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)
    tlp = Column(String, nullable=False)
    tag = Column(String, nullable=True)
    source = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)

    def __init__(self, value, type, tlp, tag, source, added_on):
        self.value = value
        self.type = type
        self.tlp = tlp
        self.tag = tag
        self.source = source
        self.added_on = added_on


class Whitelist(db.Model):
    __tablename__ = 'whitelist'

    id = Column(Integer, primary_key=True)
    element = Column(String, nullable=False)
    type = Column(String, nullable=False)
    source = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)

    def __init__(self, element, type, source, added_on):
        self.element = element
        self.type = type
        self.source = source
        self.added_on = added_on


class MISPInst(db.Model):
    __tablename__ = 'misp'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    apikey = Column(String, nullable=False)
    verifycert = Column(Boolean, nullable=False)
    added_on = Column(DateTime, nullable=False)
    last_sync = Column(DateTime, nullable=True)

    def __init__(self, name, url, key, ssl, added_on, last_sync):
        self.name = name
        self.url = url
        self.apikey = key
        self.verifycert = ssl
        self.added_on = added_on
        self.last_sync = last_sync
