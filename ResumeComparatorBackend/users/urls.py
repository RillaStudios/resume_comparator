from django.urls import path
from .views import register, login, logout, view_profile, update_profile, delete_user, change_password, protected_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', view_profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/delete/', delete_user, name='delete_user'),
    path('profile/changepass/', change_password, name='change_password'),
    path('protected/', protected_view, name='protected_view'),
]