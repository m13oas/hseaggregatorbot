import telegram
from telegram.utils.request import Request
import requests
import config
from io import BytesIO


class TelegramConnector:

    def __init__(self) -> None:
        super().__init__()
        self.bot = None

    def _is_valid_connection(self):
        try:
            self.bot.get_me()
            return True
        except Exception:
            return False

    def _auth(self):
        for url in self._get_proxy_list():
            pr_dict = {'proxy_url': 'https://{}'.format(url)}
            print(pr_dict)
            request = Request(**pr_dict)
            self.bot = telegram.Bot(token=config.TOKEN, request=request)
            if self._is_valid_connection():
                break

    @staticmethod
    def _get_proxy_list():
        link = config.TELEGRAM_PROXY_LIST_URL
        return requests.get(link).text.split('\n')

    def send_message(self, message):
        self._send_message(str(message.body))
        for attachment in message.attachments:
            self._send_attachment(attachment)

    def _send_message(self, text):
        if not self._is_valid_connection():
            self._auth()

        self.bot.send_message(config.CHAT_ID, text)

    def _send_attachment(self, file):
        if not self._is_valid_connection():
            self._auth()

        wrapped_data = BytesIO(file.data)
        self.bot.send_document(config.CHAT_ID, document = wrapped_data, filename= file.name)