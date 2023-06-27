import sys
sys.path.insert(1, '../')

import unittest

from sqlalchemy import text
from CreateSQLData import CreateSQLData, Networks
from RetrieveSQLData import RetrieveSQLData

config_path = '../inputs.ini'

class SQLTest(unittest.TestCase):

    sql_db = CreateSQLData(config_path)
    
    def test_sql(self):
        self.sql_db.add_networks()

        with self.sql_db.session_scope() as session:
            name = 'test_name'
            networks = session.query(Networks).filter_by(NETWORK_ID=name)
            n_networks = 0
            for network in networks:
                n_networks += 1
                assert str(network) == "<Networks('test_name')>"
            assert n_networks == 1

        # clear table
        self.sql_db.delete_tables()

if __name__ == "__main__":
    unittest.main()
