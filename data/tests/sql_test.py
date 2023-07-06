import unittest
from sqlalchemy import text
from CreateSQLData import CreateSQLData, Networks
from RetrieveSQLData import RetrieveSQLData

config_path = '../inputs.ini'

class SQLTest(unittest.TestCase):

    def setUp(self):
        creator   = CreateSQLData(config_path)
        retriever = RetrieveSQLData(config_path)

        creator.add_networks()

    def tearDown(self):
        # clear table
        self.creator.delete_tables()

    def test_retrieve_sql_data(self):
        """ test the retrieval of a test Network in the Networks table
        """
        pass

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

if __name__ == "__main__":
        unittest.main()
