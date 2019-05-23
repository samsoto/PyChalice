from core.dao.entities import Base, SensorData, Sensor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from core.models.request2 import Request2
from core.dao.db_utils import Queryable, SessionFactory
from sqlalchemy import func
from typing import List
from core import config


def get_sensor_data(req: Request2) -> List[SensorData]:
    activate_query_extensions()
    dbcontext: Session = get_database_context()
    return dbcontext \
        .query(SensorData) \
        .filter(SensorData.sensor_id == req.id if req.id is not None else True) \
        .filter(SensorData.timestamp >= req.start_ts if req.start_ts is not None else True) \
        .filter(SensorData.timestamp <= req.end_ts if req.end_ts is not None else True) \
        .filter_if(lambda: SensorData.sensor_id == req.id, req.id is not None) \
        .filter_if(lambda: SensorData.timestamp >= req.start_ts, req.start_ts is not None) \
        .filter_if(lambda: SensorData.timestamp <= req.end_ts, req.end_ts is not None) \
        .offset(req.offset) \
        .limit(req.limit) \
        .all()


def get_sensor_data2():
    activate_query_extensions()
    session = get_database_context()
    return session.query(Sensor, SensorData) \
        .with_entities(
            Sensor,
            Sensor.id.label("sensor_id"),
            SensorData.timestamp.label("timestamp2"),
            func.sum(SensorData.value).label("sum_value")) \
        .join(SensorData, Sensor.id == SensorData.sensor_id) \
        .group_by(Sensor.id, SensorData.timestamp) \
        .order_by(SensorData.timestamp.desc()) \
        .to_list()


class Foobar:

    def __init__(self, **kwargs):
        self.sensor_id = kwargs.get('sensor_id')
        self.timestamp = kwargs.get('timestamp')
        self.sum_value = kwargs.get('sum_value')


def activate_query_extensions():
    Query.filter_if = filter_if
    Query.to_list = to_list
    Query.select = select


def select(self, *entities):
    return self.with_entities(*entities)


def to_list(self):
    print(self)
    col_meta = self.column_descriptions
    result = self.all()
    col_names = [meta['name'] for meta in col_meta]
    result = [dict(zip(col_names, x)) for x in result]
    return result


def filter_if(self, criterion, condition: bool) -> Query:
    if condition:
        return self.filter(criterion())
    return self


def get_database_context() -> Session:
    conn_str = config.db['db_conn_string']
    engine = create_engine(conn_str)
    Base.metadata.bind = engine
    db_session = sessionmaker()
    db_session.bind = engine
    return db_session()
