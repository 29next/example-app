from urllib import response
import requests
from django.conf import settings

class Api(object):

    def __init__(self, store_id, access_token):
        self.base_url = 'https://{}.29next.store/api/admin/'.format(store_id)
        self.access_token = access_token

    def _build_url(self, path):
        return '{}{}'.format(self.base_url, path)

    def _default_headers(self):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token),
        }
        return headers

    def _get(self, path):
        headers = self._default_headers()
        url = self._build_url(path)
        response = requests.get(url, headers=headers)
        return response

    def _post(self, path, data):
        headers = self._default_headers()
        url = self._build_url(path)
        response = requests.post(url, json=data, headers=headers)
        return response

    def create_webhook(self, events, name, target):
        path = 'webhooks/'
        data = {
            'events': events,
            'name': name,
            'target': target,
            'secret_key': settings.WEBHOOK_SECRET
        }
        response = self._post(path, data)
        return response

    def get_orders(self):
        path = 'orders/'
        return self._get(path)


    def get_products(self):
        path = 'products/'
        return self._get(path)
