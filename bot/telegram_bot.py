import requests


class TelegramBot:
    def __init__(self) -> None:
        self.token = "TOKEN"
        self.name = "BOTNAME"
        self.chat_ids = self.get_all_chats()
        # self.chat_ids.append('550364925') # it is myks chat

    def send(self, message):
        for chat_id in self.chat_ids:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url).json()

    def get_all_chats(self):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        res = requests.get(url).json()
        chat_ids = map(lambda result: result['message']['chat']['id'], res['result'])
        return list(chat_ids)


if __name__ == "__main__":
    bot = TelegramBot()
    bot.get_all_chats()
    bot.send('test')
