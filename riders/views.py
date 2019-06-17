from django.shortcuts import render, redirect
from .models import Route

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


def riders_index(request):
    routes = Route.objects.all()
    return render(request, 'riders/index.html', {'routes': routes})

def route_query_AM(request):
    # add default values in .GET()
    potential_routes = Route.objects.filter(
        departureTime=request.GET['arrivalTime']
        ).filter(
        departureLocation=request.GET['departure']
        ).filter(
        arrivalLocation=request.GET['destination']
        )
    return render(request, 'riders/index.html', {'routes': potential_routes})
    # for route_AM in potential_routes:
    #     if route_AM.users.count() < route_AM.car.maxOccupancy:
    #         return render(request, 'riders/index.html', {'route_AM': route_AM})

def route_query_PM(request):
    # add default values in .GET()
    potential_routes = Route.objects.filter(
        departureTime=request.GET['arrivalTime']
        ).filter(
        departureLocation=request.GET['departure']
        ).filter(
        arrivalLocation=request.GET['destination']
        )
    return render(request, 'riders/index.html', {'routes': potential_routes})
    # for route_PM in potential_routes:
    #     if route_PM.users.count() < route_PM.car.maxOccupancy:
    #         return render(request, 'riders/index.html', {'routes_PM': route_PM})

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
class RouteCreate(LoginRequiredMixin, CreateView):
    model = Route
    fields = ['name', 'departureLocation', 'departureTime', 'arrivalLocation']
    success_url = '/riders'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RouteDetail(LoginRequiredMixin, DetailView):
    model = Route

class RouteUpdate(LoginRequiredMixin, UpdateView):
    model = Route
    fields = ['name', 'departureLocation', 'departureTime', 'arrivalLocation']

class RouteDelete(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = '/riders/'