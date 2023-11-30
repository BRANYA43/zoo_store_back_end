from uuid import uuid4

from django.db import models


class UUIDMixin(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        max_length=10,
        primary_key=True,
        unique=True
    )

    class Meta:
        abstract = True
