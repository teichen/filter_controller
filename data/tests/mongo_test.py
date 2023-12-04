import unittest
from sqlalchemy import text
from CreateMongoData import CreateMongoData
from RetrieveMongoData import RetrieveMongoData
from datetime import datetime

config_path = './inputs.ini'

class MongoTest(unittest.TestCase):
    def setUp(self):
        self.creator = CreateMongoData(config_path)

        carrier_name  = 'test_name'
        carrier_phase = 0.5 # cycles
        measurement_time  = datetime(2005, 6, 1, 0, 0)

        measurements = [{'carrier_name': carrier_name, 'carrier_phase': carrier_phase, 
                'measurement_time': measurement_time}]

        self.creator.create_measurements(measurements)

        self.retriever = RetrieveMongoData(config_path)

    def tearDown(self):
        self.creator.delete_documents()
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
            measurements['test_name'][measurement_time] = doc['carrier_phase']

        test_dict = {'test_name': {datetime(2005, 6, 1, 0, 0): 0.5}}

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

