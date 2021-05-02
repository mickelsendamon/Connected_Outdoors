from django.db import models
import re

# Create your models here.


class UserManager(models.Manager):
    def basic_validation(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 1:
            errors["first_name"] = "The first name field can't be empty!"
        if len(post_data['last_name']) < 1:
            errors["last_name"] = "The last name field can't be empty!"
        if len(post_data['password']) < 8:
            errors["password_short"] = "The password should be at least 8 characters!"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = ("Invalid email address!")
        users_with_email = User.objects.filter(email=post_data['email'])
        if len(users_with_email) >= 1:
            errors['email_duplicate'] = "Email taken already, use another email!"
        if post_data['password'] != post_data['password_conf']:
            errors['password_no_match'] = "The password and password confirmation doesn't match!"
        return errors


class ActivityManager(models.Manager):
    def basic_validation(self, post_data):
        errors = {}
        if len(post_data['name']) < 1:
            errors["name"] = "The name field can't be empty!"
        return errors


class SuggestedEquipmentManager(models.Manager):
    def basic_validation(self, post_data):
        errors = {}
        if len(post_data['name']) < 1:
            errors["name"] = "The name field can't be empty!"
        if len(post_data['description']) < 5:
            errors["description"] = "The description has to be at least 5 characters long!"
        return errors


class AdventureManager(models.Manager):
    def adventure_validation(self, post_data):
        errors = {}
        if len(post_data['location']) < 1:
            errors["location"] = "The location field can't be empty!"
        if len(post_data['distance']) < 1:
            errors["distance"] = "The distance field can't be empty!"
        if len(post_data['duration']) < 1:
            errors["duration"] = "The duration field can't be empty!"
        if len(post_data['meeting_location']) < 1:
            errors["meeting_location"] = "The meeting location field can't be empty!"
        if len(post_data['description']) < 10:
            errors["description"] = "The description has to be at least 10 characters long!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20, default="visitor")
    objects = UserManager()


class Activity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="")
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
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='adventures')
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organized_adventures')
    participants = models.ManyToManyField(
        User, related_name='participated_adventures')
    suggested_equipment = models.ManyToManyField(
        SuggestedEquipment, related_name='suggested_for')
    objects = AdventureManager()
