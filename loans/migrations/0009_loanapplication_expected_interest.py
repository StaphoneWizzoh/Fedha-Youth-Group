# Generated by Django 4.0 on 2022-12-15 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0008_alter_loanrepayment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='expected_interest',
            field=models.FloatField(default=0),
        ),
    ]
