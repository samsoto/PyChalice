from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime


def as_dict(obj):
    mydict = {}
    if isinstance(obj, datetime):
        return str(obj)
    if isinstance(obj.__class__, DeclarativeMeta):
        for c in obj.__table__.columns:
            name = c.name
            value = getattr(obj, c.name)
            if isinstance(value, datetime):
                value = str(value)
            mydict.update({name: value})
    return mydict


def parse_datetime(ts):
    if ts is not None:
        return datetime.strptime(ts, '%Y-%m-%d')
    return None
