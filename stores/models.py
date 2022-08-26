from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.urls import reverse

from .api.admin import Api

User = get_user_model()


class Store(models.Model):
    reference_id = models.CharField(max_length=200, unique=True)
    custom_checkout_message = models.CharField(max_length=300, blank=True)
    api_token = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.reference_id

    def get_absolute_url(self):
        return reverse('stores:detail', args=[self.id])


class StoreUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store} - {self.user}'

    class Meta:
        app_label = 'stores'
        verbose_name = _('Store User')


@receiver(post_save, sender=Store)
def update_store_settings(sender, instance, created, **kwargs):
    if not created and instance.reference_id and instance.api_token:
        data = {
            'example_app_custom_checkout_message': instance.custom_checkout_message
        }
        Api(instance.reference_id, instance.api_token).update_app_settings(data=data)
