from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Add more paths for different views as needed
    path('add_budget/', views.add_budget, name='add_budget'),
    path('set_budget/', views.set_budget, name='set_budget'),
]
