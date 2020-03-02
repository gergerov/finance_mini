from Dbj import Dbj
from Config import db
import logging

module_logger = logging.getLogger("Server.Unit")


class Unit(object):
    __ID__ = ''
    __USER__ = ''
    __NAME__ = ''
    __DELETED__ = ''
    __EMPTY__ = ''
    __result__ = ''

    def getID(self, user, name):

        logger = logging.getLogger("Server.Unit.getID")
        logger.info('Попытка получить ID категории, параметры: %s %s', user, name)

        self.__USER__ = user
        self.__NAME__ = name
        self.check_in_base()

        if self.__EMPTY__ == True:

            logger.info('В БД нет категории у пользователя, параметры: %s %s', user, name)

            self.__result__ = 'empty'
            return self.__result__

        elif self.__EMPTY__ == False:

            if self.__DELETED__ == 0:
                logger.info('Получено ID категории, параметры: %s', self.__ID__)
                self.__result__ = 'ok'
                return self.__ID__

            elif self.__DELETED__ == 1:
                logger.info('В БД категория у пользователя удалена')
                self.__result__ = 'deleted'
                return self.__result__

    def run(self, user, name, command_type):
        logger = logging.getLogger("Server.Unit.run")
        self.__USER__ = user
        self.__NAME__ = name

        logger.info('Инициация обработки команд unit, параметры: %s %s', user, name)

        self.check_in_base()

        if command_type == 'add_unit':

            self.add_unit()

            logger.info('Ветвь обработки: %s', command_type)
            logger.info('Результат обработки: %s', self.__result__)

            return self.__result__

        elif command_type == 'del_unit':

            self.del_unit()

            logger.info('Ветвь обработки: %s', command_type)
            logger.info('Результат обработки: %s', self.__result__)

            return self.__result__

    def add_unit(self):

        if self.__EMPTY__ == True:

            self.insert_new()
            self.__result__ = 'new'

        elif self.__EMPTY__ == False:

            if self.__DELETED__ == 1:

                self.restore()
                self.__result__ = 'restore'

            elif self.__DELETED__ == 0:

                self.__result__ = 'exists'

    def del_unit(self):

        if self.__EMPTY__ == True:

            self.__result__ = 'not exist'

        elif self.__EMPTY__ == False:

            if self.__DELETED__ == 1:

                self.__result__ = 'already deleted'

            elif self.__DELETED__ == 0:

                self.delete()
                self.__result__ = 'deleted'

    def check_in_base(self):

        sql = 'select ID, DELETED from units where USER = ? and name = ?'
        params = self.__USER__, self.__NAME__

        logger = logging.getLogger("Server.Unit.check_in_base")
        logger.info('Проверка в БД, параметры: %s %s', sql, params)

        dbj = Dbj(sql, params)
        data = dbj.ReadOne()
        logger.info('Результат из БД: %s ', data)

        if data is None:

            self.__EMPTY__ = True

        else:

            self.__EMPTY__ = False
            self.__ID__ = str(data[0])
            self.__DELETED__ = data[1]

    def insert_new(self):

        logger = logging.getLogger("Server.Unit.insert_new")

        sql = 'insert into units (user, name) values (?,?)'
        params = self.__USER__, self.__NAME__

        logger.info('Добавление категории в БД, параметры : %s %s', sql, params)

        dbj = Dbj(sql, params)
        dbj.Write()

    def restore(self):

        logger = logging.getLogger("Server.Unit.restore")

        sql = 'update units set deleted = 0 where id = ?'
        params = self.__ID__

        logger.info('Восстановление категории в БД, параметры : %s %s', sql, params)

        dbj = Dbj(sql, params)
        dbj.Write()

    def delete(self):

        logger = logging.getLogger("Server.Unit.delete")

        sql = 'update units set deleted = 1 where id = ?'
        params = self.__ID__

        logger.info('Удаление категории в БД, параметры : %s %s', sql, params)

        dbj = Dbj(sql, params)
        dbj.Write()
