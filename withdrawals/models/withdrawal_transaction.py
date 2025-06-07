from django.db import models
from merchants.models import Merchant, MerchantUser
from wallets.models import Wallet

class WithdrawalTransaction(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='withdrawal_transactions')
    user = models.ForeignKey(MerchantUser, on_delete=models.CASCADE, related_name='withdrawal_transactions')
    from_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='withdrawal_transactions')
    to_address = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    txid = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "withdrawal_transactions"
        indexes = [
            models.Index(fields=["merchant", "status"]),
            models.Index(fields=["requested_at"]),
        ]
    def __str__(self):
        return f"{self.merchant.name} | {self.user.user_uid} | {self.amount} USDT | {self.status}"
    def is_successful(self):
        return self.status == 'completed'
    def is_pending(self):
        return self.status == 'pending'
    def is_processing(self):
        return self.status == 'processing'
    def is_failed(self):
        return self.status == 'failed'
    def mark_as_completed(self, txid=None):
        self.status = 'completed'
        self.txid = txid
        self.processed_at = models.DateTimeField(auto_now=True)
        self.save()
    def mark_as_failed(self, error_message=None):
        self.status = 'failed'
        self.error_message = error_message
        self.processed_at = models.DateTimeField(auto_now=True)
        self.save()
    def mark_as_processing(self):
        self.status = 'processing'
        self.processed_at = models.DateTimeField(auto_now=True)
        self.save()
    def mark_as_pending(self):
        self.status = 'pending'
        self.processed_at = None
        self.txid = None
        self.error_message = None
        self.save()
    def get_wallet_address(self):
        return self.from_wallet.get_address() if self.from_wallet else 'Unknown Wallet Address'
    def get_wallet_name(self):
        return self.from_wallet.get_merchant_name() if self.from_wallet else 'Unknown Wallet'
    def get_wallet_id(self):
        return self.from_wallet.id if self.from_wallet else None
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
    def get_amount(self):
        return self.amount if self.amount else 0
    def get_status_display(self):
        return dict(self._meta.get_field('status').choices).get(self.status, 'Unknown Status')
    def get_requested_at(self):
        return self.requested_at if self.requested_at else 'No Request Time'
    def get_processed_at(self):
        return self.processed_at if self.processed_at else 'Not Processed Yet'
    def get_error_message(self):
        return self.error_message if self.error_message else 'No Error Message'
    def get_transaction_details(self):
        return {
            'transaction_id': self.get_transaction_id(),
            'amount': str(self.get_amount()),
            'status': self.get_status_display(),
            'requested_at': self.get_requested_at(),
            'processed_at': self.get_processed_at(),
            'error_message': self.get_error_message(),
            'wallet_address': self.get_wallet_address(),
            'merchant_name': self.get_merchant_name(),
            'user_uid': self.get_user_uid()
        }