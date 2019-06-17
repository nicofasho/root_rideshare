from django.shortcuts import render, redirect
from .models import Route, Location

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

def route_search(request):
    locations = Location.objects.all()
    return render(request, 'riders/search.html', {'locations': locations})

def route_query(request):
    pass

class RouteDetail(LoginRequiredMixin, DetailView):
    model = Route

class RouteUpdate(LoginRequiredMixin, UpdateView):
    model = Route
    fields = ['name', 'departureLocation', 'departureTime', 'arrivalLocation']

class RouteDelete(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = '/riders/'