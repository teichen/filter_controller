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
        db_name = str(config['mongo']['name'])
        db_collection = str(config['mongo']['collection'])

        # start a mongo session
        mc = MongoClient(url, uuidRepresentation='pythonLegacy')
        db = mc[db_name][db_collection]

        # create input measurements

        input_name  = 'test_name'
        input_value = 1.0
        input_time  = datetime(2005, 6, 1, 0, 0)

        inputs = {'input_name': input_name, 'input_value': input_value, 'input_time': input_time}

        # add data to mongo session
        db.insert_one(inputs)
        
        # close mongo session


