import configparser
from pymongo import MongoClient

class RetrieveMongoData:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ base class for Mongo Data Retrieval
        """
        config = configparser.ConfigParser()
        config.read('inputs.ini')

        url = str(config['mongo']['address'])
        db_name = str(config['mongo']['name'])
        db_collection = str(config['mongo']['collection'])

        # start a mongo session
        mc = MongoClient(url, uuidRepresentation='pythonLegacy')
        db = mc[db_name][db_collection]

        # retrieve data
        start_time = 
        stop_time  = 
        query = {'$or': ['start_time': {'$lte': start_time}, 'stop_time': {'$gte': stop_time}, ]}
        results = {'input_name': 0, 'input_value': 0, 'input_time': 0}
        cursor = db.find(query, results)

        # write to disk


