from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('aboutus', views.aboutus, name='aboutus'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('register/', views.register, name='register'),
	path('profile/<int:pk>/', views.profile, name='profile'),
	path('assign_id/', views.assign, name='assign'),
	path('release/', views.release, name='release'),
	path('update_mobile/<int:pk>/', views.update_mobile, name='update-mobile'),
]
