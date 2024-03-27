from django.contrib import admin
from django.urls import path
from .views import index, Login, Signup

urlpatterns = [
    path('', index,name = 'homepage'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view()),

]
