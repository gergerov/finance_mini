checktoken = ''
secretkey = ''
accesstoken = ''
host = '' # на текущий момент для тестов
port = '' # на текущий момент для тестов


# здесь путь надо редактировать
db = "db.db"
users = []
admins = []

commands = [{'Text': 'добавить пользователя', 'Len': 21, 'Type': 'add_user', 'Value': int},
            {'Text': 'удалить пользователя', 'Len': 20, 'Type': 'del_user', 'Value': int},
            {'Text': 'добавить категорию', 'Len': 18, 'Type': 'add_unit', 'Value': str},
            {'Text': 'удалить категорию', 'Len': 17, 'Type': 'del_unit', 'Value': str},
            {'Text': 'статистика день', 'Len': 15, 'Type': 'stat_d', 'Value': str},
            {'Text': 'статистика месяц', 'Len': 16, 'Type': 'stat_m', 'Value': str},
            {'Text': '1', 'Len': 0, 'Type': 'add_op', 'Value': list},
            {'Text': '1', 'Len': 0, 'Type': 'error', 'Value': None},
            {'Text': 'список категорий', 'Len': 16, 'Type': 'list_unit', 'Value': int}]

results = {'new': 'Категория успешно добавлена',
            'restore': 'Удаленная категория по запросу добавления восстановлена',
            'exists': 'Категория уже существует',
            'not exist': 'Категория не существует',
            'already deleted': 'Категория уже удалена',
            'deleted': 'Категория удалена',
            'deleted_unit': 'Невозможно добавить операцию : указанная категория удалена',
            'not_unit': 'Невозможно добавить операцию : указанная категория не существует',
            'add_op': 'Операция добавлена',
            'not_data': 'Нет данных по запросу',
            'error': 'неизвестная ошибка'}

test = {'type': 'message_new', 'object': {'message': {'date': 1582317985, 'from_id': 1, 'id': 827, 'out': 0, 'peer_id': 1, 'text': 'статистика месяц 100', 'conversation_message_id': 550, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'], 'keyboard': True, 'inline_keyboard': True, 'lang_id': 0}}, 'group_id': 1, 'event_id': 'f85570a54e25f4e68e7205a94ff6a269e1754752', 'secret': 'x1'}


