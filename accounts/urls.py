from django.urls import path , include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('logedin/' , views.logedin , name='logedin'),
    path('logedout/' , views.logedout , name='logedout'),
    path('Register/' , views.Register , name='Register'),
]
