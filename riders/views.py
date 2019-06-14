from django.shortcuts import render
from .models import Route

# Create your views here.
def home(request):
	return render(request, 'home.html')

def riders_index(request):
	routes = Route.objects.all()
	return render(request, 'riders/index.html', {'routes': routes})