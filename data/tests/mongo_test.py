import unittest
from sqlalchemy import text
from CreateMongoData import CreateMongoData
from RetrieveMongoData import RetrieveMongoData
from datetime import datetime

config_path = './inputs.ini'

class MongoTest(unittest.TestCase):
    def setUp(self):
        self.creator = CreateMongoData(config_path)

        measurement_name  = 'test_name'
        measurement_value = 1.0
        measurement_time  = datetime(2005, 6, 1, 0, 0)

        measurements = [{'measurement_name': measurement_name, 'measurement_value': measurement_value, 
                'measurement_time': measurement_time}]

        self.creator.create_measurements(measurements)

        self.retriever = RetrieveMongoData(config_path)

    def tearDown(self):
        self.creator.close_session()

    def test_create_mongo(self):
        """ test mongo data was created, bypassing the retrieval class
        """
        start_time = datetime(2005, 5, 29, 0, 0)
        stop_time  = datetime(2005, 6, 2, 0, 0)
        query = {'measurement_time': {'$gte': start_time, '$lt': stop_time}}
        cursor = self.creator.db.find(query)

        measurements = {}
        measurements['test_name'] = {}

        for doc in cursor:
            measurement_time = doc['measurement_time']
            measurements['test_name'][measurement_time] = doc['measurement_value']

        test_dict = {'test_name': {datetime(2005, 6, 1, 0, 0): 1.0}}

        self.assertDictEqual(measurements, test_dict)

    def test_retrieve_mongo(self):
        """ test retrieval of mongo data
        """
        start_time = datetime(2005, 5, 29, 0, 0)
        stop_time  = datetime(2005, 6, 2, 0, 0)
        measurements = self.retriever.retrieve_data(start_time, stop_time)

        assert 'test_name' in measurements
        assert len(measurements) == 1

if __name__ == "__main__":
    unittest.main()

