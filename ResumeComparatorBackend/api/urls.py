from django.urls import path
from api.views import ItemsView

urlpatterns = [
    path('items/', ItemsView.as_view(), name='items'),
]