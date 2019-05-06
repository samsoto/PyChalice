from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from typing import TypeVar, List, Callable
from core.dao.entities import Base
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from core import config

T = TypeVar('T')


class Queryable:

    def __init__(self, session: Session, query: Query=None):
        self.session = session
        self.query = query or session.query

    def query_from(self, *entities) -> 'Queryable':
        q = self.session.query(*entities)
        return Queryable(self.session, q)

    def select(self, *entities) -> 'Queryable':
        q = self.query.with_entities(*entities)
        return Queryable(self.session, q)

    def where(self, condition) -> 'Queryable':
        q = self.query.filter(condition)
        return Queryable(self.session, q)

    def join(self, table, on) -> 'Queryable':
        q = self.query.join(table, on)
        return Queryable(self.session, q)

    def group_by(self, *group) -> 'Queryable':
        q = self.query.group_by(*group)
        return Queryable(self.session, q)

    def order_by(self, order_by, direction: str='asc') -> 'Queryable':
        if direction == 'asc':
            return Queryable(self.session, self.query.order_by(asc(order_by)))
        return Queryable(self.session, self.query.order_by(desc(order_by)))

    def page_by(self, offset: int, limit: int) -> 'Queryable':
        q = self.query.offset(offset).limit(limit)
        return Queryable(self.session, q)

    def to_list(self) -> List[T]:
        print(self)
        col_meta = self.query.column_descriptions
        result = self.query.all()
        col_names = [meta['name'] for meta in col_meta]
        result = [dict(zip(col_names, row)) for row in result]
        return result


class SessionFactory:

    @staticmethod
    def new() -> Session:
        conn_str = config.db['db_conn_string']
        engine = create_engine(conn_str)
        Base.metadata.bind = engine
        db_session = sessionmaker()
        db_session.bind = engine
        session = db_session()
        return session
