from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('donate/', views.donate, name='donate'),
    path('my-donations/', views.my_donations, name='my_donations'),
    #to remove
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
