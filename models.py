from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Subbanker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile

class Application(models.Model):
    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    father = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    regnumber = models.CharField(max_length=100, null=True, blank=True)
    occup = models.CharField(max_length=100, null=True, blank=True)
    income = models.CharField(max_length=100, null=True, blank=True)
    limit = models.CharField(max_length=100, default='Not Updated Yet', null=True, blank=True)
    image1 = models.FileField(max_length=100, null=True, blank=True)
    image2 = models.FileField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=200, default='Not Updated Yet', null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

class About(models.Model):
    pagetitle = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.pagetitle

class Contact(models.Model):
    pagetitle = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    timing = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.pagetitle

class Trackinghistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.remark
