import unittest
from sqlalchemy import text
import getpass
from CreateSQLData import CreateSQLData, Networks
from RetrieveSQLData import RetrieveSQLData

config_path = './inputs.ini'

class SQLTest(unittest.TestCase):

    def setUp(self):
        user = getpass.getuser()
        config_paths = [config_path, '/Users/' + str(user) + '/.mysql.ini']
        self.creator   = CreateSQLData(config_paths)
        self.retriever = RetrieveSQLData(config_paths)

        self.creator.add_networks()

    def tearDown(self):
        # clear table
        #self.retriever.delete_networks()
        self.retriever.close_session()
        self.creator.delete_tables()
        self.creator.close_session()

    def test_create_sql_data(self):
        """ test the creation of a test Network in the Networks table
        """
        with self.creator.session_scope() as session:
            name = 'test_name'
            networks = session.query(Networks).filter_by(NETWORK_ID=name)
            n_networks = 0
            for network in networks:
                n_networks += 1
                assert str(network) == "<Networks('test_name')>"
            assert n_networks == 1

    def test_retrieve_sql_data(self):
        """ test the retrieval of a test Network in the Networks table
        """
        network_list = self.retriever.get_data()

        n_networks = 0
        for network in network_list:
            n_networks += 1
            assert str(network) == "<Networks('test_name')>"
        assert n_networks == 1

if __name__ == "__main__":
        unittest.main()
