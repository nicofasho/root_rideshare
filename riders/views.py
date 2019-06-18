from django.shortcuts import render, redirect
from .models import Route, Location, Profile

# Auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Login Required Mixins / Decorators
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# ClassBased Views imports
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# Create your views here.

def home(request):
    return render(request, 'home.html')


@login_required
def riders_index(request):
    curr_profile = Profile.objects.get(user=request.user)
    routes = curr_profile.route_set.all()
    return render(request, 'riders/index.html', {'routes': routes})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('riders_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# TODO: just gonna add these here for now, we're definitely going to have to customize this
# class RouteCreate(LoginRequiredMixin, CreateView):
#     model = Route
#     fields = ['name', 'departureLocation', 'departureTime', 'arrivalLocation']
#     success_url = '/riders'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


@login_required
def route_search(request):
    locations = Location.objects.all()
    return render(request, 'riders/search.html', {'locations': locations})


@login_required
def route_query(request):
    # TO DO: add default values in .GET() [x]
    # TO DO: add range to arrival time from departure time [x]
    potential_routes = Route.objects.filter(
        departureTime=request.GET['arrival']
        ).filter(
        departureLocation=request.GET['departure']
        ).filter(
        arrivalLocation=request.GET['destination']
        )
    # TO DO: can add similar functionality to the model instead or utilize F expressions
    # TO DO: Models update later to "profiles"
    # TO DO: logic to selecting carpool with fewest occupied seats, retrieve only on employer
    curr_profile = Profile.objects.get(user=request.user)
    for route in potential_routes:
        if route.users.count() < route.car.maxOccupancy:
            route.users.add(curr_profile)
            break
    return redirect('riders_index')

# TO DO: Add a remove from route function
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


class RouteUpdate(LoginRequiredMixin, UpdateView):
    model = Route
    fields = ['name', 'departureLocation', 'departureTime', 'arrivalLocation']


class RouteDelete(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = '/riders/'

