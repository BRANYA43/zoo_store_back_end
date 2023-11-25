from uuid import uuid4

from django.db import models


class UUIDMixin(models.Model):
    """
    The mixin sets uuid as primary key for model
    """
    uuid = models.UUIDField(default=uuid4, unique=True, max_length=20, primary_key=True)

    class Meta:
        abstract = True
