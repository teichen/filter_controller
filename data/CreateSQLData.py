from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser

class CreateSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ base class for SQL Data Creation
        """
        config = configparser.ConfigParser()
        config.read('inputs.ini')

        url = str(config['sql']['address'])

        # start a sql session
        engine  = create_engine(url, encoding='utf-8', convert_unicode=True, pool_size=30, pool_recycle=3600)
        session_interface = sessionmaker(bind=engine)
        session = scoped_session(session_interface)()

        session.commit() # persist permanently to disk

        # create input measurements

        inputs = []
        inputs.append(single_measurement())

        # add data to sql session

        session.add_all(inputs)
        session.commit()

        # close sql session

        session.close()
