# Generated by Django 5.0.4 on 2024-11-13 10:50

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
        ('trip', '0008_alter_trip_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2024, 11, 13, 11, 50, 53, 117084)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='currencies_rates',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='currency.currencyrates'),
            preserve_default=False,
        ),
    ]