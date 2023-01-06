from django.db import models

from members.models import Registration


class MemberShares(models.Model):
    member_name = models.ForeignKey(Registration, on_delete=models.CASCADE)
    date_of_contribution = models.DateTimeField(auto_now_add=True)
    month_of_contribution = models.DateField(auto_now_add=True, unique_for_year=True)
    amount = models.FloatField(default=500, help_text="Should be 500 and above.")

    class Meta:
        verbose_name_plural = 'Member Shares'

    def __str__(self):
        return self.member_name or None
    # def __complex__(self):
    #     return self.member_name
