from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class RetrieveSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ base class for SQL Data Retrieval
        """
        pass

