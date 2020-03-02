# DataBaseJob
import pypyodbc
from Config import db
import logging
import sqlite3

module_logger = logging.getLogger("Server.Dbj")


class Dbj(object):
    def __init__(self, sql, params=None):
        self.sql = sql
        self.params = params

    def Write(self):
        logger = logging.getLogger("Server.Dbj.Write")
        try:
            logger.info('Попытка подключения к БД: %s', db)
            Conn = sqlite3.connect(db)
            Curs = Conn.cursor()

            if self.params is None:
                try:
                    logger.info('Попытка записи данных в БД: ' + self.sql)
                    Curs.execute(self.sql)
                    Conn.commit()
                    Conn.close()

                except Exception as e:
                    logger.error('Попытка записи данных в БД не удалась: %s', e)
                    Conn.close()

            elif self.params is not None:
                try:
                    logger.info('Попытка записи данных в БД: ' + self.sql)
                    Curs.execute(self.sql, self.params)
                    Conn.commit()
                    Conn.close()

                except Exception as e:
                    logger.error('Попытка записи данных в БД не удалась: %s', e)
                    Conn.close()

        except Exception as e:
            logger.error('Попытка подключения к БД не удалась: %s', e)

    def ReadOne(self):
        logger = logging.getLogger("Server.Dbj.ReadOne")
        try:
            logger.info('Попытка подключения к БД: %s', db)
            Conn = sqlite3.connect(db)
            Curs = Conn.cursor()

            if self.params is None:
                logger.info('Попытка чтения данных из БД: ' + self.sql)
                Curs.execute(self.sql)
                Data = Curs.fetchone()

                if Data != -1:
                    Conn.commit()
                    Conn.close()
                    return Data
                else:
                    Conn.close()
                    return Data

            elif self.params is not None:
                logger.info('Попытка чтения данных из БД: ' + self.sql)
                Curs.execute(self.sql, self.params)
                Data = Curs.fetchone()

                if Data != -1:
                    Conn.commit()
                    Conn.close()
                    return Data
                else:
                    Conn.close()
                    return Data

            Conn.close()

        except Exception as e:
            print(e)

    def ReadAll(self):
        logger = logging.getLogger("Server.Dbj.ReadOne")
        try:
            logger.info('Попытка подключения к БД: %s', db)
            Conn = sqlite3.connect(db)
            Curs = Conn.cursor()

            if self.params is None:
                logger.info('Попытка чтения данных из БД: ' + self.sql)
                Curs.execute(self.sql)
                Data = Curs.fetchall()

                if Data != -1:
                    Conn.commit()
                    Conn.close()
                    return Data
                else:
                    Conn.close()
                    return Data

            elif self.params is not None:
                logger.info('Попытка чтения данных из БД: ' + self.sql)
                Curs.execute(self.sql, self.params)
                Data = Curs.fetchall()

                if Data != -1:
                    Conn.commit()
                    Conn.close()
                    return Data
                else:
                    Conn.close()
                    return Data

            Conn.close()

        except Exception as e:
            print(e)