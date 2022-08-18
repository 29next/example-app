import jwt


from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from ..models import Store, StoreUser


class StoreJWTAuthBackend(ModelBackend):

    def authenticate(self, request, token):
        try:
            user_data = jwt.decode(
                token, settings.CLIENT_SECRET, audience=settings.CLIENT_ID, algorithms=["HS256"])
            user_email = user_data.get('user_email', None)
            store_id = user_data.get('store').split('.', 1)[0]
            user, created = User.objects.get_or_create(email=user_email, username=user_email)
            store = Store.objects.filter(reference_id=store_id).first()
            # Add the user to store users
            StoreUser.objects.get_or_create(user=user, store=store)
            return user

        except jwt.ExpiredSignatureError:
            # TO DO: handle JWT tokens that are expired
            return None

