# Generated by Django 3.1.5 on 2021-01-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeapi', '0011_wallet_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
