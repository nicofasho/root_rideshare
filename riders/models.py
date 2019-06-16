from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# imports for profile creation
from django.db.models.signals import post_save
from django.dispatch import receiver


# Created models


# pretty self explanatory
class Location(models.Model):
    place = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    # override __str__ method
    def __str__(self):
        return self.name


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    maxOccupancy = models.IntegerField(
        default=4,
        validators=[MinValueValidator(2), MaxValueValidator(10)]
    )

    # override __str__ method
    def __str__(self):
        return f'A {self.color} {self.make} {self.model} with a max occupancy of {self.maxOccupancy}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # don't need username, already on built in User model
    # I'm thinking picture is just a link to imgur or something where we host the images
    picture = models.CharField(max_length=100)
    employer = models.CharField(max_length=50)
    isDriver = models.BooleanField(default=False)

    # override __str__ method
    def __str__(self):
        return self.user.username

    #methods to tie profile creation to when users are created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Route(models.Model):
    departureLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='departure')
    arrivalLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='arrival')
    users = models.ManyToManyField(Profile)
    name = models.CharField(max_length=100)
    # not sure about departureTime, since this is gonna be the same
    # time for 5 days a week, seems weird to use actual time
    # units since they snapshot a day, unless there's some
    # different way to use em
    departureTime = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)]
    )

    # override __str__ method
    def __str__(self):
        return f'A route that leaves from {self.departureLocation} at the hour of {self.departureTime} to {self.arrivalLocation}'

