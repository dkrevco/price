from browser.mvideo_curl_parameters import cookies, headers
import requests
import json

class CUrlResponse:

    def __init__(self):

        self.string = f'Type {type(CUrlResponse)}'
        self.cookies = cookies
        self.headers = headers

    def get_data(self, url, params):

        self.response = requests.get(url, params=params, cookies=cookies,
                            headers=headers).json()

        return self.response

class MVideo(CUrlResponse):

    def __init__(self):
        self.offset = 0
        super().__init__()

    def _get_products_id(self):

        params = {
            'categoryId': '205',
            'offset': f'{str(self.offset)}',
            'limit': '24',
            'filterParams': 'WyJjYXRlZ29yeSIsIiIsImlwaG9uZS05MTQiXQ==',
            'doTranslit': 'true',
        }
        self.get_data()