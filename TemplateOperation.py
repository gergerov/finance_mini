from pyparsing import *
import logging
import re

words = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
module_logger = logging.getLogger("Server.TemplateOperation")


def check_parse_operation(text):

    logger = logging.getLogger("Server.TemplateOperation.check")
    logger.info('Попытка парсинга: %s', text)

    try:
        money = Word(nums)
        unit_word = Word(words)
        unit = unit_word + ZeroOrMore(unit_word)

        command = money + unit

        result = command.parseString(text)
        logger.info('Парсинг удался: %s', result)
        return 1

    except Exception as e:
        logger.info('Парсинг не удался: %s', e)
        return -1


def get_parse_operation(text):

    logger = logging.getLogger("Server.TemplateOperation.get")
    logger.info('Попытка парсинга: %s', text)

    money = Word(nums)
    unit_word = Word(words)
    unit = unit_word + ZeroOrMore(unit_word)

    only_unit = Suppress(money) + unit
    name_unit = ' '.join(only_unit.parseString(text))

    only_money = money + Suppress(unit)
    value_money = ' '.join(only_money.parseString(text))

    logger.info('Парсинг удался')

    return value_money, name_unit



