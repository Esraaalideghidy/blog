from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',userlogin,name='login'),
    path('logout/',user_logout,name='logout'),
    path('changepassword/',change_password,name='changepassword'),
    path('profile/<int:pk>',user_profile,name='profile'),
    
    
]
