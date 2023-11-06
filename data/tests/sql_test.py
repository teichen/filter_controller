import unittest
from sqlalchemy import text
import getpass
from CreateSQLData import CreateSQLData, Devices
from RetrieveSQLData import RetrieveSQLData

config_path = './inputs.ini'

class SQLTest(unittest.TestCase):

    def setUp(self):
        user = getpass.getuser()
        config_paths = [config_path, '/Users/' + str(user) + '/.mysql.ini']
        self.creator   = CreateSQLData(config_paths)
        self.retriever = RetrieveSQLData(config_paths)

        device_names  = ['test_name']

        self.creator.add_devices(device_names)

    def tearDown(self):
        # clear table
        #self.retriever.delete_devices()
        self.retriever.close_session()
        self.creator.delete_tables()
        self.creator.close_session()

    def test_create_sql_data(self):
        """ test the creation of a test Device in the Devices table
        """
        with self.creator.session_scope() as session:
            name = 'test_name'
            devices = session.query(Devices).filter_by(NETWORK_ID=name)
            n_devices = 0
            for device in devices:
                n_devices += 1
                assert str(device) == "<Devices('test_name')>"
            assert n_devices == 1

    def test_retrieve_sql_data(self):
        """ test the retrieval of a test Device in the Devices table
        """
        device_list = self.retriever.get_data()

        n_devices = 0
        for device in device_list:
            n_devices += 1
            assert str(device) == "<Devices('test_name')>"
        assert n_devices == 1

if __name__ == "__main__":
        unittest.main()
