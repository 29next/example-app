import json
import requests

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, DetailView, View

from .api.admin import Api
from .api.webhooks import webhook_payload_validator
from .models import Store


class StoreAuthHandler(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        network_domain = self.request.GET.get('store', None)
        token = self.request.GET.get('token', None)
        store_id = network_domain.split('.', 1)[0]
        store = Store.objects.filter(reference_id=store_id, status=True)

        # Initial install flow doesnt have a token parameter
        if network_domain and not token:
            permission_setup_url = 'https://{network_domain}/oauth2/authorize/?response_type=code&'
            permission_setup_url += 'client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}'
            redirect_url= permission_setup_url.format(
                network_domain=network_domain,
                client_id=settings.CLIENT_ID,
                redirect_uri= settings.APP_DOMAIN + reverse('stores:setup'),
                scopes=settings.SCOPES
            )
            return redirect_url

        # If token is present, the app is installed on a store
        elif token:
            user = authenticate(self.request, token=token)
            if user is not None:
                auth_login(self.request, user)
                return reverse('stores:detail', args=[store.first().id])
        else:
            return '/'


class StoreAuthSetup(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        network_domain = self.request.GET.get('store', None)
        store_id = network_domain.split('.', 1)[0]
        auth_code = self.request.GET.get('code', None)

        # Request a new api access token
        url = 'https://{}/oauth2/token/'.format(network_domain)
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'redirect_uri': settings.APP_DOMAIN + reverse('stores:setup'),
            'code': auth_code
        }
        response = requests.post(url, data=data)

        # Save api access token with store for future use
        store, created = Store.objects.get_or_create(reference_id=store_id)
        store.api_token = response.json().get('access_token', '')
        store.status = True
        store.save()

        # Setup webhooks to listen to new orders and app.uninstalled event
        Api(store_id, store.api_token).create_webhook(
            settings.WEBHOOK_EVENTS, settings.WEBHOOK_NAME,
            settings.APP_DOMAIN + reverse('stores:webhook_processor')
        )
        # Redirect back to the dashboard after install flow complete
        return 'https://{}/dashboard/apps/'.format(network_domain)


class BaseStoreView(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        # Check that user belongs to the store
        user = request.user if not request.user.is_anonymous else None
        get_object_or_404(Store, pk=self.kwargs.get('pk'), storeuser__user=user)
        return super().dispatch(request, *args, **kwargs)


class StoreDetailView(BaseStoreView, DetailView):
    model = Store
    template_name = 'store-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stockrecords'] = Api(self.object.reference_id, self.object.api_token).get_stockrecords().json()
        return context


@method_decorator(csrf_exempt, name='dispatch')
class StoreWebhookProcessor(View):

    def post(self, request):
        webhook_data = json.loads(self.request.body)
        event_type = webhook_data.get('event_type', None)
        event_source_store = webhook_data.get('webhook', {}).get('store', None)
        store = Store.objects.get(reference_id=event_source_store)

        # Validate webhook data
        valid = webhook_payload_validator(
            json.dumps(webhook_data), self.request.headers.get('X-29Next-Signature', None))

        if valid and event_source_store and store:

            # Deactivate the store if app is uninstalled
            if event_type == 'app.uninstalled':
                store.status = False
                store.save()

        return HttpResponse('success')
