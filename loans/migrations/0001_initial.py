# Generated by Django 4.0 on 2022-07-15 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=15)),
                ('interest', models.FloatField(max_length=5)),
                ('repayment_period', models.IntegerField(help_text='In Years.')),
            ],
            options={
                'verbose_name_plural': 'Loan Types',
            },
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_application', models.DateTimeField(auto_now_add=True)),
                ('loan_amount', models.IntegerField(help_text='Amount you want to borrow.')),
                ('applicant_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.registration')),
                ('loan_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loantypes')),
            ],
        ),
    ]
