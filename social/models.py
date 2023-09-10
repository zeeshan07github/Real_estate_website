from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # User profile is linked to the User model using a OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Additional fields for user profile
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=50)
    
    # Privacy settings
    PROFILE_VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    )
    profile_visibility = models.CharField(max_length=10, choices=PROFILE_VISIBILITY_CHOICES, default='public')
    
    MESSAGE_PRIVACY_CHOICES = (
        ('everyone', 'Everyone'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    )
    message_privacy = models.CharField(max_length=10, choices=MESSAGE_PRIVACY_CHOICES, default='everyone')

    def __str__(self):
        return self.user.username

class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.status}'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Add this line to define the 'is_read' field

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.timestamp}'
