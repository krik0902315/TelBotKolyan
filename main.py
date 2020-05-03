import requests
import datetime
import time
import schedule


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot1110555192:AAHI9R28e0MGrA4DeX_FApNy8hV79mVbr3s/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


greet_bot = BotHandler('1110555192:AAHI9R28e0MGrA4DeX_FApNy8hV79mVbr3s')
now = datetime.datetime.now()


def main():
    new_offset = None

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        ##last_update_id = last_update['update_id']
        ##last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        def job():
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            time.sleep(2)
            greet_bot.send_message(last_chat_id, 'Как твои настроение?')
            time.sleep(2)
            greet_bot.send_message(last_chat_id, 'Надеюсь ты не влюбился.\nВедь если это так, то ты полнейший мудила!')

        schedule.every().day.at("07:30").do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()


