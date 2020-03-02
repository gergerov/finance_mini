from Dbj import Dbj
from Vkapi import get_user_name, send_message
import logging
from Config import users, commands, admins, test, results
from TemplateOperation import check_parse_operation, get_parse_operation
from Unit import Unit
from Operation import Operation
from Stat import Stat

module_logger = logging.getLogger("Server.handling")


class message_handling(object):
    __user__ = ''
    __message__ = ''
    __len_message__ = 0
    __check_user_result__ = ''
    __check_user_is_admin__ = ''
    __command_type__ = ''
    __params_text__ = []
    __handling_result__ = ''
    __answer__ = ''

    def __init__(self, js):
        self.js = js

    # из json-а берем юзера для дальнейшей проверки, берем текст для обработки команды
    def parse_json(self):

        logger = logging.getLogger("Server.handling.parse_json")
        logger.info('Попытка разбора json-сообщения: %s', self.js)

        obj = self.js['object']
        message = obj['message']
        id_vk_user = message['from_id']
        message_content = message['text']

        self.__message__ = message_content.lower()
        self.__user__ = id_vk_user
        self.__len_message__ = len(self.__message__)

    # проверяем, есть ли пользователь в конфиге
    def check_user(self):

        logger = logging.getLogger("Server.handling.check_user")
        logger.info('Проверка пользователя: %s', self.__user__)

        if self.__user__ not in users:
            self.__check_user_result__ = -1
            logger.info('Нет прав у пользователя: %s', self.__user__)
        elif self.__user__ in users:
            self.__check_user_result__ = 1
            logger.info('Пользователь прошел проверку: %s', self.__user__)

        if self.__user__ in admins:
            self.__check_user_is_admin__ = 1
        elif self.__user__ not in admins:
            self.__check_user_is_admin__ = -1

    # определяем тип команды и её параметры
    def what_command(self):

        logger = logging.getLogger("Server.handling.what_command")
        logger.info('Определение, что за команда: %s', self.__message__)

        # проверим, является ли команда командой управления

        for line in commands:
            check_text = self.__message__[0:line['Len']]
            if check_text == line['Text']:
                self.__command_type__ = line['Type']
                self.__params_text__ = self.__message__[line['Len'] + 1:self.__len_message__]

                logger.info('Команда определена как: %s', self.__command_type__)
                logger.info('Параметры: %s', self.__params_text__)

        # проверим, является ли команда командой добавления операции

        if self.__command_type__ == '':
            var = check_parse_operation(self.__message__)

            if var == -1:
                self.__command_type__ = 'error'
                self.__params_text__ = ''

                logger.info('Команда определена как: %s', self.__command_type__)
                logger.info('Параметры: %s', self.__params_text__)


            elif var == 1:
                self.__command_type__ = 'add_op'
                self.__params_text__ = get_parse_operation(self.__message__)

                logger.info('Команда определена как: %s', self.__command_type__)
                logger.info('Параметры: %s', self.__params_text__)

    def units_handling(self):
        unit = Unit()
        self.__handling_result__ = unit.run(self.__user__, self.__params_text__, self.__command_type__)

    def operations_add(self):
        unit = Unit()
        unitID = unit.getID(self.__user__, self.__params_text__[1])

        if unitID == 'empty':
            self.__handling_result__ = 'not_unit'

        elif unitID == 'deleted':
            self.__handling_result__ = 'deleted_unit'

        else:

            operation = Operation()
            operation.create(self.__user__, self.__params_text__[1], self.__params_text__[0])
            operation.insert()

            self.__handling_result__ = 'add_op'

    def stat_check_params(self):
        try:
            int(self.__params_text__)
            return True
        except:
            return False

    def stat_handling(self):

        if self.stat_check_params() == True:

            stat = Stat(self.__user__, self.__params_text__, self.__command_type__)
            self.__answer__ = stat.run()

            if self.__answer__ == '0':
                self.__handling_result__ = 'not data'

            else:
                self.__handling_result__ = 'exists data'

        else:
            self.__handling_result__ = 'error'

    def return_all(self):
        print('Пользователь : ' + str(self.__user__))
        print('Сообщение : ' + self.__message__)
        print('Длинна сообщения : ' + str(self.__len_message__))
        print('Результат проверки пользователя : ' + str(self.__check_user_result__))
        print('Пользователь является администратором : ' + str(self.__check_user_is_admin__))
        print('Тип команды : ' + self.__command_type__)
        print('Параметры команды : ' + str(self.__params_text__))
        print('Результат обработки : ' + self.__handling_result__)

    def get_answer(self):
        if self.__handling_result__ == 'exists data':
            self.__answer__ = self.__answer__
        else:
            self.__answer__ = results[self.__handling_result__]

    def send_answer(self):
        send_message(self.__user__, self.__answer__)

    def run(self):

        self.parse_json()
        self.check_user()
        self.what_command()

        if self.__command_type__ == 'add_unit' or self.__command_type__ == 'del_unit':
            self.units_handling()
        elif self.__command_type__ == 'add_op':
            self.operations_add()
        elif self.__command_type__ == 'stat_m' or self.__command_type__ == 'stat_d':
            self.stat_handling()

        else:
            self.__handling_result__ = 'error'

        self.get_answer()
        self.send_answer()
