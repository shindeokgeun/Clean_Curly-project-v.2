from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='benefit_benefit'),
]