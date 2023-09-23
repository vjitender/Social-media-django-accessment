import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    modified_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True