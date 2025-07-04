# Generated by Django 5.2.2 on 2025-06-07 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchants', '0001_initial'),
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawalTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_address', models.CharField(max_length=64)),
                ('amount', models.DecimalField(decimal_places=6, max_digits=20)),
                ('txid', models.CharField(blank=True, max_length=128, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('from_wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='withdrawal_transactions', to='wallets.wallet')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal_transactions', to='merchants.merchant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal_transactions', to='merchants.merchantuser')),
            ],
            options={
                'db_table': 'withdrawal_transactions',
                'indexes': [models.Index(fields=['merchant', 'status'], name='withdrawal__merchan_a8a836_idx'), models.Index(fields=['requested_at'], name='withdrawal__request_325b0d_idx')],
            },
        ),
    ]
