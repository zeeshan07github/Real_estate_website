from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path("" , views.home , name='home'),
    path("property_list" , views.property_list , name='property_list'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/delete/', views.property_delete, name='property_delete'),
    path('property/<int:property_id>/unknown_delete/', views.property_delete, name='unknown_delete'),
    path('agent/<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('contact/'  , views.contact , name = 'contact'),
    path('about/'  , views.about , name = 'about'),
    path('addnewproperty/'  , views.property_create , name = 'addnewproperty'),
    path('addnewagent/'  , views.agent_create , name = 'addnewagent'),
    path('filter/', views.property_filter, name='filter'),
    path('delete_account/' , views.Delete_account , name='Delete_account'),
    
    
]


