from Dbj import Dbj
import datetime


class Stat(object):
    __user__ = ''
    __num__ = ''
    __type__ = ''
    __result__ = ''

    def __init__(self, user, num, type):
        self.__user__ = user
        self.__num__ = num
        self.__type__ = type

    def run(self):

        if self.__type__ == 'stat_d':
            self.list_operation_day()
        elif self.__type__ == 'stat_m':
            self.list_operation_month()
        elif self.__type__ == 'list_unit':
            self.list_unit()
        else:
            self.__result__ = 'error'

        return self.__result__

    def list_unit(self):

        sql = 'select ID, NAME from units where USER = ? and DELETED = 0'
        params = [self.__user__]

        dbj = Dbj(sql, params)
        data = dbj.ReadAll()

        if not data:
            self.__result__ = '0'

        else:

            for line in data:
                self.__result__ += str(line[0]) + ' ' + str(line[1]) + '\n'

    def list_operation_day(self):

        now = datetime.datetime.now()

        d_now = now.day
        m_now = now.month
        y_now = now.year

        d_start = d_now - int(self.__num__)
        if d_start < 0:
            d_start = 0

        sql = 'select UNIT, sum(MONEY) from operations ' \
              'where USER = ? and m = ? and y = ? and d between ? and ?' \
              'group by UNIT'

        params = self.__user__, m_now, y_now, d_start, d_now

        dbj = Dbj(sql, params)
        data = dbj.ReadAll()

        if not data:
            self.__result__ = '0'

        else:
            for line in data:
                self.__result__ += '\t' + str(line[0]) + ' ' + str(line[1]) + ' руб\n'

    def list_operation_month(self):
        now = datetime.datetime.now()

        d_now = now.day
        m_now = now.month
        y_now = now.year

        m_start = m_now - int(self.__num__)
        if m_start < 0:
            m_start = 0

        sql = 'select UNIT, sum(MONEY) from operations ' \
              'where USER = ? and y = ? and m between ? and ?' \
              'group by UNIT'

        params = self.__user__, y_now, m_start, m_now

        dbj = Dbj(sql, params)
        data = dbj.ReadAll()

        if not data:
            self.__result__ = '0'

        else:
            for line in data:
                self.__result__ += '\t' + str(line[0]) + ' ' + str(line[1]) + ' руб\n'
