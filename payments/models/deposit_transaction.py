from django.db import models
from merchants.models import Merchant, MerchantUser
from wallets.models import Wallet

class DepositTransaction(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='deposit_transactions')
    user = models.ForeignKey(MerchantUser, on_delete=models.CASCADE, related_name='deposit_transactions')
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='deposit_transactions')
    transaction_number = models.CharField(max_length=100)  # Provided by merchant
    expected_amount = models.DecimalField(max_digits=20, decimal_places=6)
    received_amount = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    txid = models.CharField(max_length=128, null=True, blank=True)  # Incoming USDT txid
    confirmed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('failed', 'Failed'),
            ('expired', 'Expired')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    sweep_txid = models.CharField(max_length=128, null=True, blank=True)  # Outgoing sweep txid

    class Meta:
        db_table = "deposit_transactions"
        indexes = [
            models.Index(fields=["merchant", "status"]),
            models.Index(fields=["transaction_number"]),
            models.Index(fields=["created_at"]),
        ]
        unique_together = ('merchant', 'transaction_number')
    def __str__(self):
        return f"{self.merchant.name} | {self.transaction_number} | {self.status} | {self.expected_amount} USDT"
    def is_successful(self):
        return self.status == 'confirmed' and self.confirmed
    def is_pending(self):
        return self.status == 'pending' and not self.confirmed
    def is_failed(self):
        return self.status == 'failed' or (self.confirmed and not self.is_successful())
    def is_expired(self):
        return self.status == 'expired' or (self.confirmed and not self.is_successful())
    def mark_as_confirmed(self):
        self.status = 'confirmed'
        self.confirmed = True
        self.confirmed_at = models.DateTimeField(auto_now=True)
        self.save()
    def mark_as_failed(self):
        self.status = 'failed'
        self.confirmed = False
        self.save()
    def mark_as_expired(self):
        self.status = 'expired'
        self.confirmed = False
        self.save()
    def update_received_amount(self, amount):
        self.received_amount = amount
        if amount >= self.expected_amount:
            self.mark_as_confirmed()
        else:
            self.mark_as_failed()
        self.save()
    def get_wallet_address(self):
        return self.wallet.get_address() if self.wallet else 'Unknown Wallet Address'
    def get_wallet_name(self):
        return self.wallet.get_merchant_name() if self.wallet else 'Unknown Wallet'
    def get_wallet_id(self):
        return self.wallet.id if self.wallet else None
    def get_merchant_name(self):
        return self.merchant.name if self.merchant else 'Unknown Merchant'
    def get_merchant_id(self):
        return self.merchant.id if self.merchant else None
    def get_user_uid(self):
        return self.user.user_uid if self.user else 'Unknown User'
    def get_user_id(self):
        return self.user.id if self.user else None
    def get_transaction_id(self):
        return self.txid if self.txid else 'No Transaction ID'
    def get_sweep_txid(self):
        return self.sweep_txid if self.sweep_txid else 'No Sweep Transaction ID'
    def get_transaction_number(self):
        return self.transaction_number if self.transaction_number else 'No Transaction Number'
    def get_expected_amount(self):
        return self.expected_amount if self.expected_amount else 0
    def get_received_amount(self):
        return self.received_amount if self.received_amount else 0
    def get_status_display(self):
        return dict(self._meta.get_field('status').choices).get(self.status, 'Unknown Status')
    def get_transaction_details(self):
        return {
            'transaction_number': self.get_transaction_number(),
            'expected_amount': str(self.get_expected_amount()),
            'received_amount': str(self.get_received_amount()),
            'status': self.get_status_display(),
            'created_at': self.created_at,
            'confirmed_at': self.confirmed_at,
            'txid': self.get_transaction_id(),
            'sweep_txid': self.get_sweep_txid(),
            'wallet_address': self.get_wallet_address(),
            'merchant_name': self.get_merchant_name(),
            'user_uid': self.get_user_uid()
        }