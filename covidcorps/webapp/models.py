from django.db import models
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from django.contrib.auth.models import AbstractUser
from .utils.enums import USStates, AssignmentStatus

# Create your models here.

class Account(AbstractUser):

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

    @staticmethod
    def init(email, password):
        """
        Creates a new Account instance, but hashes the password
        on creation
        """
        return Account(email=email, password=make_password(password))

class CorpsMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=10)
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(
        max_length=2, 
        choices=USStates.choices(),
    )
    zipcode = models.CharField(max_length=5)
    active = models.BooleanField(default=True)

    # Assignments NtoM
    deployments = models.ManyToManyField('Deployment', through='Assignment')

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class CorpsMemberPhoneNumber(models.Model):
    corpsmember = models.ForeignKey(CorpsMember, on_delete=models.CASCADE)
    sms_ok = models.BooleanField()
    value = models.CharField(max_length=20)
    preferred = models.BooleanField()
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class CorpsMemberEmail(models.Model):
    corpsmember = models.ForeignKey(CorpsMember, on_delete=models.CASCADE)
    value = models.EmailField()
    preferred = models.BooleanField()
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class Location(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(
        max_length=2, 
        choices=USStates.choices(),
    )
    zipcode = models.CharField(max_length=5)

    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class LocationContact(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    prefix = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=10)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class LocationContactPhoneNumber(models.Model):
    location_contact = models.ForeignKey(LocationContact, on_delete=models.CASCADE)
    sms_ok = models.BooleanField()
    value = models.CharField(max_length=20)
    preferred = models.BooleanField()
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class LocationContactEmail(models.Model):
    location_contact = models.ForeignKey(LocationContact, on_delete=models.CASCADE)
    value = models.EmailField()
    preferred = models.BooleanField()
    active = models.BooleanField(default=True)

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)


class Deployment(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    members_needed = models.IntegerField()
    description = models.TextField()

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)

class Assignment(models.Model):
    corpsmember = models.ForeignKey(CorpsMember, on_delete=models.DO_NOTHING)
    deployment = models.ForeignKey(Deployment, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=10,
        choices=AssignmentStatus.choices(),
    )

    # Timestamps
    created_ts = models.DateTimeField(auto_now_add=True)
    last_ts = models.DateTimeField(auto_now=True)