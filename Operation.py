from Dbj import Dbj
from Config import db
import logging
import datetime

class Operation(object):

    __ID__ = ''
    __USER__ = ''
    __UNIT__ = ''
    __money__ = ''
    __d__ = ''
    __m__ = ''
    __y__ = ''
    __DELETED__ = ''
    __params_insert__ = []

    def create(self, user, unit, money):

        self.__USER__ = user
        self.__UNIT__ = unit
        self.__money__ = money

        self.__d__ = datetime.datetime.now().day
        self.__m__ = datetime.datetime.now().month
        self.__y__ = datetime.datetime.now().year

        self.__params_insert__ = self.__USER__, self.__UNIT__, self.__money__, \
                                 self.__d__, self.__m__, self.__y__

    def insert(self):

        sql = 'insert into operations (USER, UNIT, MONEY, D, M, Y)' \
              'values (?,?,?,?,?,?)'

        dbj = Dbj(sql, self.__params_insert__)
        dbj.Write()





