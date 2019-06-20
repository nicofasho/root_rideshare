from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# for maps api requests
import requests
import environ
import os
import json
environ.Env()
environ.Env.read_env()

api_key = os.environ['GOOGLE_MAPS_API_KEY']

# imports for profile creation
from django.db.models.signals import post_save
from django.dispatch import receiver


# Created models
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
            Profile.objects.get_or_create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Route(models.Model):
    departureLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='departure')
    arrivalLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='arrival')
    users = models.ManyToManyField(Profile)
    name = models.CharField(max_length=100)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    departureTime = models.TimeField(auto_now=False, auto_now_add=False)
    imgURL = models.CharField(max_length=1000, default='', blank=True)

    class Meta:
        ordering = ['departureTime']

    # override __str__ method
    def __str__(self):
        return f'Route leaves from {self.departureLocation} at {self.departureTime} to {self.arrivalLocation} in {self.car}'

    def save(self, *args, **kwargs):
        line_response = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={self.departureLocation.name}&destination={self.arrivalLocation.name}&key={api_key}")
        line = line_response.json()['routes'][0]['overview_polyline']['points']

        self.imgURL = f"https://maps.googleapis.com/maps/api/staticmap?size=300x200&markers=color:white%7Clabel:A%7C{self.departureLocation.name}&markers=color:green%7Clabel:B%7C{self.arrivalLocation.name}&path=enc:{line}&key={api_key}"
        super(Route, self).save(*args, **kwargs)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)