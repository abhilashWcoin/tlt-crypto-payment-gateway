from django.db import models
from merchants.models import Merchant, MerchantUser
from wallets.models import Wallet

class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('consolidation', 'Consolidation'),   # sweep from sub-wallet to hot wallet
        ('gas', 'Gas/Fee'),                   # explicit gas usage, if you want to record it separately
    ]
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='wallet_transactions')
    user = models.ForeignKey(MerchantUser, on_delete=models.CASCADE, null=True, blank=True, related_name='wallet_transactions')
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='wallet_transactions')
    # Links to business objects (nullable, because not all WalletTransactions will map)
    deposit = models.ForeignKey('payments.DepositTransaction', null=True, blank=True, on_delete=models.SET_NULL)
    withdrawal = models.ForeignKey('withdrawals.WithdrawalTransaction', null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    txid = models.CharField(max_length=128, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)  # USDT or token amount
    gas_used = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)  # TRX spent as gas
    status = models.CharField(
        max_length=20,
        choices=[('pending','Pending'),('confirmed','Confirmed'),('failed','Failed')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "wallet_transactions"
        indexes = [
            models.Index(fields=["merchant", "type"]),
            models.Index(fields=["wallet"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.merchant.name} | {self.get_type_display()} | {self.amount} | {self.status}"
    def save(self, *args, **kwargs):
        if self.type == 'gas' and not self.gas_used:
            raise ValueError("Gas used must be specified for gas transactions")
        if self.type in ['deposit', 'withdrawal'] and not self.amount:
            raise ValueError("Amount must be specified for deposit and withdrawal transactions")
        super().save(*args, **kwargs)
    def get_transaction_type_display(self):
        return dict(self.TRANSACTION_TYPES).get(self.type, 'Unknown Transaction Type')
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
    def is_successful(self):
        return self.status == 'confirmed'
    def is_pending(self):
        return self.status == 'pending'
    def is_failed(self):
        return self.status == 'failed'
    def mark_as_confirmed(self):
        self.status = 'confirmed'
        self.confirmed_at = models.DateTimeField(auto_now=True)
        self.save()
    def mark_as_failed(self):
        self.status = 'failed'
        self.save()
    def mark_as_pending(self):
        self.status = 'pending'
        self.confirmed_at = None
        self.save()
    def get_transaction_id(self):
        return self.txid if self.txid else 'No Transaction ID'
    def get_amount(self):
        return self.amount if self.amount else 0
    def get_gas_used(self):
        return self.gas_used if self.gas_used else 0
    def get_description(self):
        return self.description if self.description else 'No Description'
    def set_description(self, description):
        self.description = description
        self.save()
    def get_created_at(self):
        return self.created_at if self.created_at else 'No Creation Date'
    def get_confirmed_at(self):
        return self.confirmed_at if self.confirmed_at else 'Not Confirmed Yet'
    def get_status_display(self):
        return dict(self._meta.get_field('status').choices).get(self.status, 'Unknown Status')
    def get_transaction_details(self):
        return {
            'transaction_id': self.get_transaction_id(),
            'amount': str(self.get_amount()),
            'gas_used': str(self.get_gas_used()),
            'status': self.get_status_display(),
            'created_at': self.get_created_at(),
            'confirmed_at': self.get_confirmed_at(),
            'description': self.get_description(),
            'wallet_address': self.get_wallet_address(),
            'merchant_name': self.get_merchant_name(),
            'user_uid': self.get_user_uid()
        }
    
