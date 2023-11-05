import abc
import configparser
from datetime import datetime, timedelta
import pandas as pd
import uuid
from pymongo import MongoClient

class CreateMongoData:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config_path):
        """ base class for Mongo Data (measurements) Creation
        """
        config = configparser.ConfigParser()
        config.read(config_path)

        url = str(config['mongo']['address'])
        db_name = str(config['mongo']['db_name'])
        db_collection = str(config['mongo']['db_collection'])

        # start a mongo session
        self.mc = MongoClient(url, uuidRepresentation='pythonLegacy')
        self.db = self.mc[db_name][db_collection]

    def create_measurements(self, measurements):
        """ create measurements

        Args:
            measurements (list): list of measure dictionaries each containing measurement_name,
                                 measurement_value, measurement_time
        Returns: None
        """
        # add data to mongo session
        self.db.insert_many(measurements)

    def close_session(self):
        """ close mongo session
        """
        self.mc.close()

