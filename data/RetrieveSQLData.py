from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class RetrieveSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ base class for SQL Data Retrieval
        """
        pass

    # TODO: write to disk

    # TODO: delete NETWORKS SQL table and database
    # with session_scope(sql_data_uri) as session:
    #       session.query('Networks').delete('fetch')
    #       session.commit()
