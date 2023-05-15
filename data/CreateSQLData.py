from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser
from datetime import datetime, timedelta
import pandas as pd
import uuid

class CreateSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ base class for SQL Data (Network Definitions) Creation
        """
        config = configparser.ConfigParser()
        config.read('inputs.ini')

        url = str(config['sql']['address'])

        # start a sql session
        engine  = create_engine(url, encoding='utf-8', convert_unicode=True, pool_size=30, pool_recycle=3600)
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
        """ create network definition blob

        Args:
            network_name (str): measurement network name

        Returns:
        """
        network_row = "<NETWORK('%s', '%.4f')>" % (network_name)

        return network_row


