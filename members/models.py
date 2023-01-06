from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Registration(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=14, null=True)
    last_name = models.CharField(max_length=14, null=True)
    age = models.IntegerField(help_text="Age between 18 and 35 years", )
    registration_fee = models.FloatField(max_length=5,
                                         help_text="Required registration amount for each member.")
    contact_number = models.CharField(max_length=14, unique=True)
    id_number = models.IntegerField(unique=True)
    photo = models.ImageField(null=True, blank=True, upload_to="members/photos/",
                              help_text="Used for ease in identification")

    def __str__(self):
        return self.first_name + " " + self.last_name


class Guarantor(models.Model):
    guarantor_name = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="Guarantor")
    beneficiary_name = models.ManyToManyField(Registration, related_name="Beneficiary")
    amount_guaranteed = models.IntegerField(help_text="Amount you want to guarantee your beneficiary")
    date = models.DateTimeField(auto_now_add=True)

    def __complex__(self):
        return self.guarantor_name.get_attname()


class MemberExit(models.Model):
    name = models.ForeignKey(Registration, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    confirmation = models.BooleanField(default=False, blank=False)
    is_cleared = models.BooleanField(default=False, blank=False)
