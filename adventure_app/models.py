from django.db import models


# Create your models here.
class UserManager(models.Manager):
    def basic_validation(self, post_data):
        errors = []
        # todo validate post_data
        return errors


class ActivityManager(models.Manager):
    def basic_validation(self, post_data):
        errors = []
        # todo validate post_data
        return errors


class SuggestedEquipmentManager(models.Manager):
    def basic_validation(self, post_data):
        errors = []
        # todo validate post_data
        return errors


class AdventureManager(models.Manager):
    def basic_validation(self, post_data):
        errors = []
        # todo validate post_data
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()


class Activity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField()pip
    objects = ActivityManager()


class SuggestedEquipment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    objects = SuggestedEquipmentManager()


class Adventure(models.Model):
    location = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    distance = models.CharField(max_length=255)
    skill_level = models.CharField(max_length=255)
    adventure_start = models.DateTimeField()
    duration = models.CharField(max_length=255)
    meeting_location = models.CharField(max_length=255)
    description = models.TextField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='adventures')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_adventures')
    participants = models.ManyToManyField(User, related_name='participated_adventures')
    suggested_equipment = models.ManyToManyField(SuggestedEquipment, related_name='suggested_for')
    objects = AdventureManager()
