from django.db import models
from .merchant import Merchant

class MerchantUser(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='users')
    user_uid = models.CharField(max_length=64)

    class Meta:
        unique_together = ('merchant', 'user_uid')
        db_table = "merchant_users"
        indexes = [
            models.Index(fields=['merchant']),
            models.Index(fields=['user_uid']),
        ]
    def __str__(self):  
        return f"{self.merchant.name} | {self.user_uid}"
