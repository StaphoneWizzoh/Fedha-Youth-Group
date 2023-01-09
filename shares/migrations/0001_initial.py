# Generated by Django 4.0 on 2022-07-15 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberShares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_contribution', models.DateTimeField(auto_now_add=True)),
                ('month_of_contribution', models.DateField(auto_now_add=True, unique_for_year=True)),
                ('amount', models.FloatField(default=500, help_text='Should be 500 and above.')),
                ('member_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.registration')),
            ],
            options={
                'verbose_name_plural': 'Member Shares',
            },
        ),
    ]