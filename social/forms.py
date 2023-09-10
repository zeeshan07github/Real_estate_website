from django import forms
from django.contrib.auth.models import User
from .models import *
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'location', 'profile_visibility', 'message_privacy']

class FriendshipRequestForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ['receiver']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']


class SendFriendRequestForm(forms.Form):
    receiver_username = forms.CharField()

class AcceptRejectFriendRequestForm(forms.Form):
    action = forms.CharField()
    friendship_id = forms.IntegerField()
