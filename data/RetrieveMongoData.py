import abc
import configparser
from pymongo import MongoClient

class RetrieveMongoData:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config_file):
        """ base class for Mongo Data Retrieval

        Args:
            config_file (str)
        """
        config = configparser.ConfigParser()
        config.read(config_file)

        url = str(config['mongo']['address'])
        db_name = str(config['mongo']['db_name'])
        db_collection = str(config['mongo']['db_collection'])

        # start a mongo session
        mc = MongoClient(url, uuidRepresentation='pythonLegacy')
        self.db = mc[db_name][db_collection]

    def retrieve_data(self, start_time, stop_time):
        """ retrieve data

        Args:
            start_time (datetime)
            stop_time (datetime)
        Returns:
            measurements (dict): dictionary of measurement values by name, time
        """
        query = {'measurement_time': {'$gte': start_time, '$lt': stop_time}}
        cursor = self.db.find(query)

        measurements = {}

        for doc in cursor:
            measurement_name = doc['measurement_name']
            
            if not (measurement_name in measurements):
                measurements[measurement_name] = {}
            measurement_time = doc['measurement_time']
            measurements[measurement_name][measurement_time] = doc['measurement_value']

        return measurements

    def write_data(self):
        """ write to disk
        """
        # TODO
        pass
