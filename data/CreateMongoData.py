from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser
from datetime import datetime, timedelta
import pandas as pd
import uuid
from pymongo import MongoClient

class CreateMongoData:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ base class for Mongo Data (inputs) Creation
        """
        config = configparser.ConfigParser()
        config.read('inputs.ini')

        url = str(config['mongo']['address'])

        # start a mongo session
        # create input measurements

        input_name  = 'test_name'
        input_value = 1.0
        input_time  = datetime(2005, 6, 1, 0, 0)


        # add data to mongo session
        # close mongo session


