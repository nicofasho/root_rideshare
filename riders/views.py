import datetime

from django.shortcuts import render, redirect
import uuid
import boto3
from .models import Route, Location, Profile, Photo

# Profile Create form import
from .forms import ProfileForm

# Auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Login Required Mixins / Decorators
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# ClassBased Views imports
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# AMZN photo storage
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcoll2'

# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def riders_index(request):
    curr_profile = Profile.objects.get(user=request.user)
    routes = curr_profile.route_set.all()
    return render(request, 'riders/index.html', {'routes': routes}, )


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_create', username=user.username)
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def profile_create(request, username):
    error_message = ''
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile.update(picture='text',employer=request.POST['employer'])
            return redirect('route_create')
        else:
            error_message = 'Invalid Profile info - try again'
    form = ProfileForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/profileinfo.html', context)
            

class RouteAdd(LoginRequiredMixin, CreateView):
    model = Route
    fields = ['car', 'users', 'departureLocation', 'name', 'arrivalLocation', 'departureTime' ]
    success_url = '/routes/'


@login_required
def route_search(request):
    locations = Location.objects.all()
    return render(request, 'riders/search.html', {'locations': locations})


@login_required
def route_query(request):
    # Not expecting seconds to be entered with Materialize's Timepicker
    time_obj = datetime.datetime.strptime(request.GET['arrival'], '%H:%M')
    time_interval = datetime.timedelta(minutes=15)
    time_obj_earlier = time_obj - time_interval
    time_obj_later = time_obj + time_interval
    time_string_earlier = time_obj_earlier.strftime('%H:%M')
    time_string_later = time_obj_later.strftime('%H:%M')

    potential_routes = Route.objects.filter(
        departureTime__gte=time_string_earlier
        ).filter(
        departureTime__lte=time_string_later
        ).filter(
        departureLocation=request.GET['departure']
        ).filter(
        arrivalLocation=request.GET['destination']
        )
    curr_profile = Profile.objects.get(user=request.user)
    for route in potential_routes:
        if route.users.count() < route.car.maxOccupancy:
            route.users.add(curr_profile)
            break
    return redirect('riders_index')


@login_required
def route_unassoc(request, route_id):
    curr_profile = Profile.objects.get(user=request.user)
    curr_route = Route.objects.get(id=route_id)
    # Prevent a route from having no Profiles(Users) associated with it
    if curr_route.users.count() > 1:
        curr_route.users.remove(curr_profile)
    return redirect('route_create')

class RouteDetail(LoginRequiredMixin, DetailView):
    model = Route

class RouteDelete(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = '/routes/'

@login_required
def add_photo(request, username):
    curr_profile = Profile.objects.get(user=request.user)
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, profile_id=curr_profile.id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile_create', username=request.user.username)


@login_required
def routes_index(request):
    curr_profile = Profile.objects.get(user=request.user)
    routes = curr_profile.route_set.all()
    return render(request, 'riders/drivers_index.html', {'routes': routes})
