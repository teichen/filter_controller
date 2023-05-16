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
        start_time = datetime(2005, 5, 29, 0, 0)
        stop_time  = datetime(2005, 6, 2, 0, 0)
        query = {'input_time': {'$gte': start_time, '$lt': stop_time}}
        cursor = db.find(query)

        inputs = {}
        inputs['test_name'] = {}

        for doc in cursor:
            input_time = doc['input_time']
            inputs['test_name'][input_time] = doc['input_value']

        # write to disk


