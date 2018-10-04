# -*- coding: utf-8 -*-
"""
connect to xml server TSTWEOSQL,5876
"""
import logging
import time
import pyodbc

logger = logging.getLogger("connect")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

SERVER_NAME = 'TSTWEOSQL,5876'
DATABASE_NAME = 'IMF_EPUBS'

class Connect_SQL_Server:
    def __init__(self):
        self.__SERVER_NAME__ = SERVER_NAME
        self.__DATABASE_NAME__ = DATABASE_NAME
        try:
            self.conn = pyodbc.connect("driver={SQL Server}; server=" + \
                                   self.__SERVER_NAME__ + "; database=" + \
                                   self.__DATABASE_NAME__ + \
                                   ';Trusted_Connection=yes')
            self.cursor = self.conn.cursor()
        except:
            try:
                print('try second option')
                self.conn = pyodbc.connect('Trusted_Connection=yes',
                         driver='{SQL Server Native Client 11.0}',
                         server='%s' % self.__SERVER_NAME__,
                         database='%s' % self.__DATABASE_NAME__)
                self.cursor = self.conn.cursor()
            except Exception as e:
                logger.exception("message")
        
    def Execute_Query(self, query, name='N/A'):
        logger.info('Executing %s. Retrieving Data from Server %s Database %s'\
                    % (name, self.__SERVER_NAME__, self.__DATABASE_NAME__))
        start = time.time()
        try:
            self.cursor.execute(query)
        except Exception as e:
            logger.exception("message")
        logger.info('''Finished Retrieving Data. Took %.2f mins ''', \
                    (time.time() - start)/60)
        
    def close_connection(self):
        self.cursor.close()

if __name__ == '__main__':
    CON = pyodbc.connect('Trusted_Connection=yes',
                     driver='{SQL Server Native Client 11.0}', #driver='{SQL Server}'
                     server='%s' % SERVER_NAME,
                     database='%s' % DATABASE_NAME)

    CURSOR = CON.cursor()
    QUERY_STRING = "SELECT * FROM dbo.PUBLICATION" #get metadata table 

    CURSOR.execute(QUERY_STRING)
    
    for row in CURSOR:
        print('row = %r' % (row,))