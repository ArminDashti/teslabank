# Generated by Django 4.0.4 on 2022-06-07 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internetbank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_accounts',
            name='account_number',
            field=models.IntegerField(default=int),
            preserve_default=False,
        ),
    ]
