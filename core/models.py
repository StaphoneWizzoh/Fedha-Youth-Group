from django.db import models


class Savings(models.Model):
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)


class FixedDeposits(models.Model):
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)


