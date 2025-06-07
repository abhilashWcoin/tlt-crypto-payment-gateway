from django.db import models
from merchants.models import Merchant

class Wallet(models.Model):
    WALLET_TYPE_CHOICES = [
        ('hot', 'Hot Wallet'),
        ('sub', 'Sub-wallet'),
        ('cold', 'Cold Wallet'),
    ]
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="wallets")
    address = models.CharField(max_length=64, unique=True)
    private_key_encrypted = models.TextField()
    derivation_index = models.IntegerField(null=True, blank=True)  # for BIP44
    type = models.CharField(max_length=10, choices=WALLET_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_sweep_at = models.DateTimeField(null=True, blank=True)
    last_usdt_balance = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    last_trx_balance = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    last_balance_checked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "wallets"
        indexes = [
            models.Index(fields=["merchant", "type"]),
        ]
    def __str__(self):
        return f"{self.merchant.name} | {self.get_type_display()} | {self.address}"
    def get_balance(self):
        # Placeholder for actual balance retrieval logic
        return {
            'usdt': self.last_usdt_balance,
            'trx': self.last_trx_balance
        }
    def get_address(self):
        return self.address
    def get_private_key(self):
        # Placeholder for actual private key decryption logic
        return self.private_key_encrypted
    def get_derivation_index(self):
        return self.derivation_index if self.derivation_index is not None else 0

    def update_balances(self, usdt_balance, trx_balance):
        self.last_usdt_balance = usdt_balance
        self.last_trx_balance = trx_balance
        self.last_balance_checked_at = models.DateTimeField(auto_now=True)
        self.save()
    def update_last_sweep(self):
        self.last_sweep_at = models.DateTimeField(auto_now=True)
        self.save()
    def get_wallet_type_display(self):
        return dict(self.WALLET_TYPE_CHOICES).get(self.type, 'Unknown')
    def get_merchant_name(self):
        return self.merchant.name if self.merchant else 'Unknown Merchant'
    def get_merchant_id(self):
        return self.merchant.id if self.merchant else None
    def get_wallet_id(self):
        return self.id
    def get_wallet_address(self):
        return self.address if self.address else 'No Address'
    def get_wallet_private_key(self):
        return self.private_key_encrypted if self.private_key_encrypted else 'No Private Key'
    def get_wallet_derivation_index(self):
        return self.derivation_index if self.derivation_index is not None else 'No Derivation Index'