from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('riders/', views.riders_index, name='riders_index'),
]