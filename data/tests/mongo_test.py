import unittest
import numpy as np
from numpy import random
from sqlalchemy import text
from CreateMongoData import CreateMongoData
from RetrieveMongoData import RetrieveMongoData
from datetime import datetime

config_path = './inputs.ini'

random.seed(10)

class MongoTest(unittest.TestCase):
    def setUp(self):
        self.creator = CreateMongoData(config_path)

        self.carrier_name  = 'test_name'
        self.carrier_phase = 0.5 # cycles
        self.transmission_time  = datetime(2005, 6, 1, 0, 0)
        self.prn_code = [int(prn_element) for prn_element in np.array(np.floor(0.5 + random.rand(1023)))]

        measurements = [{'carrier_name': self.carrier_name, 'carrier_phase': self.carrier_phase, 
            'transmission_time': self.transmission_time, 'prn_code': self.prn_code}]

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
        query = {'transmission_time': {'$gte': start_time, '$lt': stop_time}}
        cursor = self.creator.db.find(query)

        measurements = {}
        measurements['test_name'] = {}

        for doc in cursor:
            transmission_time = doc['transmission_time']
            measurements['test_name'][transmission_time] = {'carrier_phase': doc['carrier_phase'], 'prn_code': doc['prn_code']}

        test_dict = {self.carrier_name: {self.transmission_time: {'carrier_phase': self.carrier_phase, 'prn_code': self.prn_code}}}

        self.assertDictEqual(measurements, test_dict)

    def test_retrieve_mongo(self):
        """ test retrieval of mongo data
        """
        start_time = datetime(2005, 5, 29, 0, 0)
        stop_time  = datetime(2005, 6, 2, 0, 0)
        measurements = self.retriever.retrieve_data(start_time, stop_time)

        assert self.carrier_name in measurements
        assert len(measurements) == 1

if __name__ == "__main__":
    unittest.main()

