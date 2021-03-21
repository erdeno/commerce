# Generated by Django 3.1.7 on 2021-03-02 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20210302_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='last_bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_bid', to=settings.AUTH_USER_MODEL),
        ),
    ]