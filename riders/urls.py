from django.urls import path, include
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('riders/', views.riders_index, name='riders_index'),
	path('riders/<int:route_id>/remove/', views.route_unassoc, name='route_unassoc'),
	path('routes/search/', views.route_search, name='route_create'),
	path('routes/search/query/', views.route_query, name='route_query'),
	path('routes/<int:pk>/', views.RouteDetail.as_view(), name='route_detail'),
	path('routes/<int:pk>/delete/', views.RouteDelete.as_view(), name='route_delete'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup', views.signup, name='signup'),
	path('accounts/<slug:username>/profilecreate', views.profile_create, name='profile_create'),
	path('accounts/<slug:username>/profilecreate/add_photo/', views.add_photo, name='add_photo'),
	path('routes/', views.routes_index, name='routes_index'),
  	path('routes/add/', views.RouteAdd.as_view(), name='route_add'),
]