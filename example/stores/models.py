from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.urls import reverse

User = get_user_model()


class Store(models.Model):
    reference_id = models.CharField(max_length=200, unique=True)
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
