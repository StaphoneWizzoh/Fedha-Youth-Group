# Generated by Django 4.0 on 2022-12-15 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0006_rename_payee_name_loanrepayment_payee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrepayment',
            name='loan_balance',
            field=models.FloatField(help_text='Your loan balance.'),
        ),
    ]
