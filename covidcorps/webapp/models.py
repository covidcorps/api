from django.db import models
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from django.contrib.auth.models import AbstractUser
from .utils import enums

# Create your models here.

class Account(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    @staticmethod
    def init(email, password):
        """
        Creates a new Account instance, but hashes the password
        on creation
        """
        account = Account(email=email)
        account.set_password(password)
        return account

class CorpsMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=10, blank=True)
    address1 = models.TextField()
    address2 = models.TextField(blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(
        max_length=2, 
        choices=enums.USStates.choices(),
    )
    zipcode = models.CharField(max_length=5)
    active = models.BooleanField(default=True)

    # Connects each CorpsMember to a category
    category = models.CharField(
        max_length=30,
        choices=enums.CorpsMemberCategories.choices(),
        default="DOCTOR",
    )

    # Assignments NtoM
    deployments = models.ManyToManyField('Deployment', through='Assignment')

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class CorpsMemberPhoneNumber(models.Model):
    corpsmember = models.ForeignKey(CorpsMember, on_delete=models.CASCADE)
    sms_ok = models.BooleanField(default=False)
    value = models.CharField(max_length=20)
    preferred = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class CorpsMemberEmail(models.Model):
    corpsmember = models.ForeignKey(CorpsMember, on_delete=models.CASCADE)
    value = models.EmailField()
    preferred = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class Location(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    address1 = models.TextField()
    address2 = models.TextField(blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(
        max_length=2, 
        choices=enums.USStates.choices(),
    )
    zipcode = models.CharField(max_length=5)

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class LocationContact(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    prefix = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=10, blank=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class LocationContactPhoneNumber(models.Model):
    location_contact = models.ForeignKey(LocationContact, on_delete=models.CASCADE)
    sms_ok = models.BooleanField(default=False)
    value = models.CharField(max_length=20)
    preferred = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class LocationContactEmail(models.Model):
    location_contact = models.ForeignKey(LocationContact, on_delete=models.CASCADE)
    value = models.EmailField()
    preferred = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class Deployment(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    members_needed = models.IntegerField()
    description = models.TextField(blank=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class Assignment(models.Model):
    corpsmember = models.ForeignKey(CorpsMember, on_delete=models.DO_NOTHING)
    deployment = models.ForeignKey(Deployment, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=10,
        choices=enums.AssignmentStatus.choices(),
    )

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)