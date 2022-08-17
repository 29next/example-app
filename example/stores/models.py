from django.db import models


class Store(models.Model):
    reference_id = models.CharField(max_length=200, unique=True)
    api_key = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.reference_id
