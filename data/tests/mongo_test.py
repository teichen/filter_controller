import unittest
from sqlalchemy import text
from CreateMongoData import CreateMongoData
from RetrieveMongoData import RetrieveMongoData
from datetime import datetime

config_path = './inputs.ini'

class MongoTest(unittest.TestCase):
    def setUp(self):
        self.mongo_db = CreateMongoData(config_path)

    def tearDown(self):
        pass

    def test_mongo(self):
        # retrieve data
        start_time = datetime(2005, 5, 29, 0, 0)
        stop_time  = datetime(2005, 6, 2, 0, 0)
        query = {'input_time': {'$gte': start_time, '$lt': stop_time}}
        cursor = self.mongo_db.db.find(query)

        inputs = {}
        inputs['test_name'] = {}

        for doc in cursor:
            input_time = doc['input_time']
            inputs['test_name'][input_time] = doc['input_value']

        test_dict = {'test_name': {datetime(2005, 6, 1, 0, 0): 1.0}}

        self.assertDictEqual(inputs, test_dict)

if __name__ == "__main__":
    unittest.main()

