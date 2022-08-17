import requests
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Store


CLIENT_ID = 'kbCWYEPXMezpXripKyDSlAO6fz4quutiaEXmh4Rx'
CLIENT_SECRET = 'BbinQTKsWtbxvNCMYEQLUs9sOtlAITPeV9Y06eBHKLjs8XPL9jZvFK8IVcsIp2VM3QyT0jxXNbd2ucpfLd1kqf6wzn9VbV00WTRj2t1huz277Si4S4XTAvnnYzfKpraL'
SCOPES = 'admin:read admin:write'


def setup(request):
    network_domain = request.GET.get('store')
    permission_setup_url = 'https://{network_domain}/oauth2/authorize/?response_type=code&'
    permission_setup_url += 'client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}'
    redirect_url= permission_setup_url.format(
        network_domain=network_domain,
        client_id=CLIENT_ID,
        redirect_uri='http://localdev.alexphelps.me:3333/stores/authcode/',
        scopes=SCOPES
    )
    return redirect(redirect_url)


def auth_code(request):
    store = request.GET.get('store')
    auth_code = request.GET.get('code')
    url = 'https://{}/oauth2/token/'.format(store)
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localdev.alexphelps.me:3333/stores/authcode/',
        'code': auth_code
    }
    response = requests.post(url, data=data)
    access_token = response.json().get('access_token', '')
    print(access_token)
    return HttpResponse('success')
