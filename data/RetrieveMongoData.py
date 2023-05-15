from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class RetrieveMongoData:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ base class for Mongo Data Retrieval
        """
        pass

    # TODO: write to disk

