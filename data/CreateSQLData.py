import abc
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from contextlib import contextmanager
import configparser
from datetime import datetime, timedelta
import pandas as pd
import uuid
import getpass
import urllib

Base = declarative_base()

class Devices(Base):
    """ SQL table class for input (measurement) device object
    """
    __tablename__ = 'Devices'

    ID = Column(Integer, primary_key=True)
    NETWORK_ID = Column(String(16), nullable=False)

    def __init__(self, NETWORK_ID):
        """
        """
        self.NETWORK_ID = NETWORK_ID

    def __repr__(self):
        """ official string representation of Devices class
        """
        return "<Devices('%s')>" % (self.NETWORK_ID)

    def __hash__(self):
        """
        """
        return hash((self.NETWORK_ID))

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
                Column('NETWORK_ID', String(16), nullable=False),
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

    def add_devices(self, device_names):
        """ create device definitions (devices of measurements)
        
        Args:
            device_names (list): list of devices providing measurements to be filtered
        """
        devices = []

        for device_name in device_names:
            devices.append(self.single_device(device_name))

        # add data to sql session
        self.session.add_all(devices)
        self.session.commit()

    def close_session(self):
        """ close SQL session
        """
        self.session.close()

    def single_device(self, device_name):
        """ create device definition class

        Args:
            device_name (str): measurement device name

        Returns:
        """
        device_row = Devices(device_name)

        return device_row


