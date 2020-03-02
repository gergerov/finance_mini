from Config import accesstoken
from vk_api.utils import get_random_id
import vk

session = vk.Session(access_token=accesstoken)
api = vk.API(session, v=5.103)


def send_message(user_id, text, att=''):
    api.messages.send(access_token=accesstoken,
                      user_id=str(user_id),
                      message=text,
                      attachment=att,
                      random_id=get_random_id())


def get_user_name(user_id):
    answer = api.users.get(user_ids=user_id, v=5.103)
    user_info = answer[0]
    return user_info['first_name'], user_info['last_name']


