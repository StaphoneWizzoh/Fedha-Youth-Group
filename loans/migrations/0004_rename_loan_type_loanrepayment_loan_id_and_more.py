# Generated by Django 4.0 on 2022-12-13 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_rename_date_of_application_loanrepayment_date_of_repayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanrepayment',
            old_name='loan_type',
            new_name='loan_id',
        ),
        migrations.AddField(
            model_name='loanrepayment',
            name='loan_balance',
            field=models.IntegerField(default=None, help_text='Your loan balance.'),
            preserve_default=False,
        ),
    ]
