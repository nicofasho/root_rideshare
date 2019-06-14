from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'home.html')

def riders_index(request):
	return render(request, 'riders/index.html')