from django.db import models


# Create your models here.
class PromotionItem(models.Model):
    promotion_id = models
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    discount = models.DecimalField(max_digits=100, decimal_places=1)
    discount_type = models.CharField(max_length=10)
    amount = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} - {self.name}'


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    promotions = models.ManyToManyField(PromotionItem)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} - {self.name}'


