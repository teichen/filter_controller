from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
import configparser
from datetime import datetime, timedelta
import pandas as pd
import uuid
import getpass

Base = declarative_base()

class Networks(Base):
    """ SQL table class for input (measurement) network object
    """
    __tablename__ = 'Networks'

    ID = Column(Integer, primary_key=True)
    NETWORK_ID = Column(String, nullable=False)

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

    def __init__(self):
        """ base class for SQL Data (Network Definitions) Creation
        """
        config = configparser.ConfigParser()
        config.read('inputs.ini')

        sql_address = str(config['sql']['address'])
        sql_user    = getpass.getuser()
        sql_pswd    = getpass.getpass(prompt='password: ')
        sql_db      = str(config['sql']['db_name'])
        sql_port    = str(config['sql']['port'])
        
        url = 'mysql+pymysql://' + sql_user + ':' + sql_pswd + '@' + sql_address +\
                ':' + sql_port + '/' + sql_db + '?charset=utf8mb4&binary_prefix=true'

        # start a sql session
        engine  = create_engine(url, pool_size=30, pool_recycle=3600)
        session_interface = sessionmaker(bind=engine)
        session = scoped_session(session_interface)()

        session.commit() # persist permanently to disk

        # create network definitions (networks of measurements)

        networks = []

        network_name  = 'test_name'

        networks.append(single_network(network_name))

        # add data to sql session

        session.add_all(networks)
        session.commit()

        # close sql session

        session.close()

    def single_network(network_name):
        """ create network definition class

        Args:
            network_name (str): measurement network name

        Returns:
        """
        network_row = Networks(network_name)

        return network_row


