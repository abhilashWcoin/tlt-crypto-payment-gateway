from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mnemonic_encrypted = models.TextField()
    hot_wallet_address = models.CharField(max_length=64, unique=True)
    hot_wallet_private_key_encrypted = models.TextField()
    deposit_min_amount = models.DecimalField(max_digits=20, decimal_places=6, default=1)
    deposit_max_amount = models.DecimalField(max_digits=20, decimal_places=6, default=10000)
    withdraw_min_amount = models.DecimalField(max_digits=20, decimal_places=6, default=1)
    withdraw_max_amount = models.DecimalField(max_digits=20, decimal_places=6, default=10000)
    callback_url = models.URLField(null=True, blank=True)
    callback_secret = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "merchants"
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]
