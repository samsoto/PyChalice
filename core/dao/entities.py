# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Sensor(Base):
    __tablename__ = 'Sensor'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)


class SensorData(Base):
    __tablename__ = 'SensorData'

    sensor_id = Column(BigInteger, primary_key=True, nullable=False)
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    value = Column(Float(53), nullable=False)



