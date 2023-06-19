import abc
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
import configparser
from datetime import datetime, timedelta
import pandas as pd
import uuid
import getpass
import urllib

Base = declarative_base()

class Networks(Base):
    """ SQL table class for input (measurement) network object
    """
    __tablename__ = 'Networks'

    ID = Column(Integer, primary_key=True)
    NETWORK_ID = Column(String(16), nullable=False)

    def __init__(self, NETWORK_ID):
        """
        """
        self.NETWORK_ID = NETWORK_ID

    def __repr__(self):
        """ official string representation of Networks class
        """
        return "<Networks('%s')>" % (self.NETWORK_ID)

    def __hash__(self):
        """
        """
        return hash((self.NETWORK_ID))

class CreateSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config_path):
        """ base class for SQL Data (Network Definitions) Creation
        
        Args:
            config_path (str): path to configuration file
        """
        config = configparser.ConfigParser()
        config.read(config_path)

        sql_address = str(config['sql']['address'])
        sql_user    = 'root' # getpass.getuser()
        sql_pswd    = getpass.getpass(prompt='password: ')
        sql_db      = str(config['sql']['db_name'])
        sql_port    = str(config['sql']['port'])
        
        sql_pswd = urllib.parse.quote(sql_pswd.encode('utf8'))

        url = 'mysql+pymysql://' + sql_user + ':' + sql_pswd + '@' + sql_address +\
                ':' + sql_port + '/' + sql_db + '?charset=utf8mb4&binary_prefix=true'

        # start a sql session
        engine  = create_engine(url, pool_size=30, pool_recycle=3600)
        if not database_exists(engine.url):
            create_database(engine.url)

        # create Networks table
        metadata_obj = MetaData()
        profile = Table(
                'Networks',
                metadata_obj,
                Column('ID', Integer, primary_key=True),
                Column('NETWORK_ID', String(16), nullable=False),
                )

        metadata_obj.create_all(engine)

        session_interface = sessionmaker(bind=engine)
        self.session = scoped_session(session_interface)()

        self.session.commit() # persist permanently to disk

    def add_networks(self):
        """ create network definitions (networks of measurements)
        """
        networks = []

        network_name  = 'test_name'

        networks.append(self.single_network(network_name))

        # add data to sql session
        self.session.add_all(networks)
        self.session.commit()

    def close_session(self):
        """ close SQL session
        """
        self.session.close()

    def single_network(self, network_name):
        """ create network definition class

        Args:
            network_name (str): measurement network name

        Returns:
        """
        network_row = Networks(network_name)

        return network_row


