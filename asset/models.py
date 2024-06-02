from django.db import models

from organization.models import Organization
from service.models import Service

# Create your models here.
class AssetModel(models.Model):
    asset = models.ImageField(upload_to='upload/')
    type = models.TextField()
    description = models.TextField()
    organization = models.ForeignKey(Organization, default=None, related_name='organizations',on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.pk}')