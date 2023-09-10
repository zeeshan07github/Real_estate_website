from django.urls import path
from . import views
app_name = 'social'  # Add this line to set the app namespace

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit_profile/<str:username>/', views.edit_profile, name='edit_profile'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('send-friend-request/<str:receiver_username>/', views.send_friend_request, name='send_friend_request'),
    
    path('accept-reject-friend-request/', views.accept_reject_friend_request, name='accept_reject_friend_request'),

    path('messaging/', views.messaging, name='messaging'),
    path('message-thread/<str:username>/', views.message_thread, name='message_thread'),
    path('privacy-settings/', views.UserProfile, name='privacy_settings'),
     path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('message/delete/all/', views.delete_all_messages, name='delete_all_messages'),

    # Add more URL patterns here:
    # For example:
    # path('search/', views.search, name='search'),
    
    # path('other-feature/', views.other_feature, name='other_feature'),
]
