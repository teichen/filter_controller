import abc
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Numeric
from contextlib import contextmanager
import configparser
from datetime import datetime, timedelta
import pandas as pd
import uuid
import getpass
import urllib

Base = declarative_base()

class Devices(Base):
    """ SQL table class for input (carrier wave) device object
    """
    __tablename__ = 'Devices'

    ID = Column(Integer, primary_key=True)
    CARRIER_ID = Column(String(16), nullable=False)
    CARRIER_FREQ = Column(Numeric(6, 2), nullable=False)

    def __init__(self, CARRIER_ID, CARRIER_FREQ):
        """
        Args:
            CARRIER_ID: device name
            CARRIER_FREQ: carrier wave frequency, either 1575.42 MHz or 1227.6 MHz
        """
        self.CARRIER_ID = CARRIER_ID
        self.CARRIER_FREQ = CARRIER_FREQ

    def __repr__(self):
        """ official string representation of Devices class
        """
        return "<Devices('%s', %.2f)>" % (self.CARRIER_ID, self.CARRIER_FREQ)

    def __hash__(self):
        """
        """
        return hash((self.CARRIER_ID, self.CARRIER_FREQ))

class CreateSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config_paths):
        """ base class for SQL Data (Device Definitions) Creation
        
        Args:
            config_paths (list): paths to configuration files
        """
        config = configparser.ConfigParser()
        config.read(config_paths)

        sql_address = str(config['sql']['address'])
        sql_user    = 'root' # getpass.getuser()
        sql_pswd    = str(config['sql']['password'])
        sql_db      = str(config['sql']['db_name'])
        sql_port    = str(config['sql']['port'])
        
        sql_pswd = urllib.parse.quote(sql_pswd.encode('utf8'))

        url = 'mysql+pymysql://' + sql_user + ':' + sql_pswd + '@' + sql_address +\
                ':' + sql_port + '/' + sql_db + '?charset=utf8mb4&binary_prefix=true'

        # start a sql session
        self.engine  = create_engine(url, pool_size=30, pool_recycle=3600)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        # create Devices table
        self.metadata_obj = MetaData()
        profile = Table(
                'Devices',
                self.metadata_obj,
                Column('ID', Integer, primary_key=True),
                Column('CARRIER_ID', String(16), nullable=False),
                Column('CARRIER_FREQ', Numeric(6, 2), nullable=False)
                )

        self.metadata_obj.create_all(self.engine)

        session_interface = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_interface)()

        self.session.commit() # persist permanently to disk

    def delete_tables(self):
        """
        """
        self.metadata_obj.drop_all(self.engine)

    @contextmanager
    def session_scope(self):
        session = self.session
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def add_devices(self, input_devices):
        """ create device definitions (carriers)
        
        Args:
            input_devices (dict): device carrier frequencies by name, measurements to be filtered
        """
        devices = []

        carrier_names = list(input_devices.keys())
        for carrier_name in carrier_names:
            carrier_freq = input_devices[carrier_name]
            devices.append(self.single_device(carrier_name, carrier_freq))

        # add data to sql session
        self.session.add_all(devices)
        self.session.commit()

    def close_session(self):
        """ close SQL session
        """
        self.session.close()

    def single_device(self, carrier_name, carrier_freq):
        """ create device definition class

        Args:
            carrier_name (str): measurement device name
            carrier_freq (float)

        Returns:
        """
        device_row = Devices(carrier_name, carrier_freq)

        return device_row


