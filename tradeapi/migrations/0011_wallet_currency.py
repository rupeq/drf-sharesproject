# Generated by Django 3.1.2 on 2021-01-18 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tradeapi', '0010_auto_20210118_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wallet', to='tradeapi.currency'),
        ),
    ]
