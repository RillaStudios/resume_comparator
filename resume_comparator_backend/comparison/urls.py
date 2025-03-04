from django.urls import path
from .views import process_text

urlpatterns = [ 
    path('process_text/', views.process_text, name='process_text'), 
    ] 