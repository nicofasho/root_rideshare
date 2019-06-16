from django.urls import path, include
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('riders/', views.riders_index, name='riders_index'),
	path('routes/create/', views.RouteCreate.as_view(), name='route_create'),
	path('routes/<int:pk>/', views.RouteDetail.as_view(), name='route_detail'),
	path('routes/<int:pk>/update/', views.RouteUpdate.as_view(), name='route_update'),
	path('routes/<int:pk>/delete/', views.RouteDelete.as_view(), name='route_delete'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup', views.signup, name='signup'),
]