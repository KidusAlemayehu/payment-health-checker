from django.db import models

# Create your models here.
class PaymentService(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
