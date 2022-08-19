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
        return requests.get(url, headers=headers)

    def _post(self, path, data):
        headers = self._default_headers()
        url = self._build_url(path)
        return requests.post(url, json=data, headers=headers)

    def create_webhook(self, events, name, target):
        path = 'webhooks/'
        data = {
            'events': events,
            'name': name,
            'target': target,
            'secret_key': settings.WEBHOOK_SECRET
        }
        return self._post(path, data)

    def get_orders(self):
        path = 'orders/'
        return self._get(path)

    def get_products(self):
        path = 'products/'
        return self._get(path)

    def get_stockrecords(self):
        path = 'stockrecords/'
        return self._get(path)
