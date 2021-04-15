from __future__ import unicode_literals
from django.db import models

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['first_name'].isalpha()) == False:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name can not be shorter than 2 characters"

        if (postData['last_name'].isalpha()) == False:
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name can not be shorter than 2 characters"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short!"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()




class StatusMaster(models.Model):
    status = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class PropertyMaster(models.Model):
    accountId = models.BigIntegerField()
    acres = models.FloatField()
    adTargetingCountyId = models.BigIntegerField()
    address = models.CharField(max_length=255)
    baths = models.BigIntegerField()
    beds = models.BigIntegerField()
    brokerCompany= models.CharField(max_length=255)
    brokerName = models.CharField(max_length=255)
    Url = models.URLField(max_length=255)
    city = models.CharField(max_length=255)
    cityID= models.BigIntegerField()
    companyLogoDocumentId = models.BigIntegerField()
    county= models.CharField(max_length=255)
    countyId = models.BigIntegerField()
    description = models.TextField(max_length=255)
    hasHouse = models.BooleanField()
    hasVideo = models.BooleanField()
    hasVirtualTour = models.BooleanField()
    hasVirtualTour = models.BigIntegerField()
    imageCount = models.BigIntegerField()
    imageAltTextDisplay = models.CharField(max_length=255)
    # PK_id = models.BigIntegerField(default=0)
    isHeadlineAd = models.BooleanField()
    lwPropertyId = models.BigIntegerField()
    isALC = models.BigIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.FloatField()
    types = models.TextField(max_length=255)
    state = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    status1 = models.CharField(max_length=255)
    zip = models.BigIntegerField()
    Rate = models.FloatField()
    NetPrAr = models.FloatField(default=0.00)
    Descrpt = models.TextField(max_length=255,default="!")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class AvgMaster(models.Model):
    # acres = models.FloatField()
    county = models.CharField(max_length=255)
    # price = models.FloatField()
    state = models.CharField(max_length=255)
    NetPrAr = models.FloatField(default=0.00)
    Rate = models.FloatField()
    UserPercentage = models.FloatField(default=0.00)
    FinaleValue = models.FloatField(default=0.00)
    accountId = models.BigIntegerField()
    acres = models.FloatField()
    adTargetingCountyId = models.BigIntegerField()
    address = models.CharField(max_length=255)
    baths = models.BigIntegerField()
    beds = models.BigIntegerField()
    brokerCompany = models.CharField(max_length=255)
    brokerName = models.CharField(max_length=255)
    Url = models.URLField(max_length=255)
    city = models.CharField(max_length=255)
    cityID = models.BigIntegerField()
    companyLogoDocumentId = models.BigIntegerField()
    countyId = models.BigIntegerField()
    description = models.TextField(max_length=255)
    hasHouse = models.BooleanField()
    hasVideo = models.BooleanField()
    hasVirtualTour = models.BooleanField()
    hasVirtualTour = models.BigIntegerField()
    imageCount = models.BigIntegerField()
    imageAltTextDisplay = models.CharField(max_length=255)
    # PK_id = models.BigIntegerField(default=0)
    isHeadlineAd = models.BooleanField()
    lwPropertyId = models.BigIntegerField()
    isALC = models.BigIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.FloatField()
    types = models.TextField(max_length=255)
    status = models.CharField(max_length=20)
    status1 = models.CharField(max_length=255)
    zip = models.BigIntegerField()
    Descrpt = models.TextField(max_length=255, default="!")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class TypeMaster(models.Model):
    class Meta:
                app_label = "socialcustom"
                managed = True
    TypeId = models.IntegerField()
    TypeName = models.CharField(max_length=255)

class Property_TypeMaster(models.Model):
        class Meta:
                app_label = "socialcustom"
                managed = True
                # unique_together = (('lwPropertyId', 'TypeId'),)
        Prop_Id2 = models.IntegerField(default=0)
        Type_Id2 = models.IntegerField(default=0)









