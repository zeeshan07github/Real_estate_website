from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django.db.models import Max


@login_required
def dashboard(request):
    # Retrieve relevant information for the dashboard
    user_profile, created = UserProfile.objects.get_or_create(user=request.user) # Assuming UserProfile is related to User via a OneToOneField
    friend_requests = Friendship.objects.filter(receiver=request.user, status='pending')
    unread_messages_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    
    context = {
        'user_profile': user_profile,
        'friend_requests': friend_requests,
        'unread_messages_count': unread_messages_count,
        # Add more relevant data as needed
    }
    
    return render(request, 'social/dashboard.html', context)


@login_required
def user_profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    # Check privacy settings
    if user_profile.profile_visibility == 'private' and user_profile.user != request.user:
        messages.error(request, "This profile is private.")
        return redirect('social:dashboard')

    # Handle profile updates
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'social/user_profile.html', {'user_profile': user_profile, 'form': form})


@login_required
def edit_profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    # Check privacy settings
    if user_profile.profile_visibility == 'private' and user_profile.user != request.user:
        messages.error(request, "This profile is private.")
        return redirect('social:dashboard')

    # Handle profile updates
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'social/edit_profile.html', {'user_profile': user_profile, 'form': form})

@login_required
def send_friend_request(request, receiver_username):
    if request.method == 'POST':
        receiver = get_object_or_404(User, username=receiver_username)
        # Check if a friendship request already exists
        existing_request = Friendship.objects.filter(sender=request.user, receiver=receiver, status='pending').first()
        
        if existing_request:
            messages.warning(request, "Friend request already sent.")
        else:
            # Create a new friendship request
            friendship_request = Friendship(sender=request.user, receiver=receiver, status='pending')
            friendship_request.save()
            messages.success(request, "Friend request sent successfully.")
    
    return redirect('social:dashboard')  # Redirect to the user's profile page

@login_required
def accept_reject_friend_request(request):
    if request.method == 'POST':
        form = AcceptRejectFriendRequestForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            friendship_id = form.cleaned_data['friendship_id']
            friendship = get_object_or_404(Friendship, id=friendship_id, receiver=request.user, status='pending')

            if action == 'accept':
                # Accept the friend request
                friendship.status = 'accepted'
                friendship.save()
                messages.success(request, "Friend request accepted.")
            elif action == 'reject':
                # Reject the friend request
                friendship.status = 'rejected'
                friendship.save()
                messages.success(request, "Friend request rejected.")
    
    return redirect('social:dashboard')  # Redirect back to the friend requests page

@login_required
def friend_requests(request):
    # Get users who are not your friends
    users_to_send_request = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=Friendship.objects.filter(
            sender=request.user, status='accepted'
        ).values('receiver_id')
    ).exclude(
        id__in=Friendship.objects.filter(
            receiver=request.user, status='accepted'
        ).values('sender_id')
    )

    # Get pending friend requests
    pending_requests = Friendship.objects.filter(receiver=request.user, status='pending')

    # Check if a request has already been sent to each user
    existing_requests = Friendship.objects.filter(sender=request.user, status='pending').values_list('receiver_id', flat=True)

    return render(request, 'social/friend_requests.html', {
        'users_to_send_request': users_to_send_request,
        'pending_requests': pending_requests,
        'existing_requests': existing_requests,
    })



@login_required
def messaging(request):
    # Retrieve user's messages
    

    # Group messages by sender and select the latest message for each sender
    messages_inbox = Message.objects.filter(receiver=request.user).values('sender').annotate(last_message=Max('timestamp'))
    
    # Retrieve the complete message objects for the latest messages
    latest_messages = Message.objects.filter(receiver=request.user, timestamp__in=messages_inbox.values('last_message'))
    
    # Fetch the users corresponding to the senders of the latest messages
    users_with_messages = User.objects.filter(id__in=messages_inbox.values('sender'))
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            content = form.cleaned_data['content']
            
            # Check if the user is allowed to send a message to the receiver
            if can_send_message(request.user, receiver):
                # Create a new message
                message = Message(sender=request.user, receiver=receiver, content=content)
                message.save()
                
                messages.success(request, "Message sent successfully.")
                return redirect('social:messaging')  # Redirect back to the messaging page after sending the message
            else:
                messages.error(request, "You cannot message this user due to privacy settings.")
    
    else:
        form = MessageForm()
    return render(request, 'social/messaging.html', {'messages_inbox': messages_inbox, 'form': form, 'latest_messages': latest_messages, 'users_with_messages': users_with_messages})
    

def can_send_message(sender, receiver):
    # Implement your logic to check if the sender is allowed to send a message to the receiver
    # This can include privacy settings, friendship status, or any other criteria
    
    # Example: Check if the receiver's message privacy allows messages from everyone
    receiver_profile = UserProfile.objects.get(user=receiver)
    if receiver_profile.message_privacy == 'everyone':
        return True
    
    # Example: Check if the sender and receiver are friends
    friendship = Friendship.objects.filter(
        (Q(sender=sender, receiver=receiver, status='accepted') |
         Q(sender=receiver, receiver=sender, status='accepted'))
    ).first()
    
    if friendship:
        return True
    
    return False


@login_required
def message_thread(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    
    # Check if users are friends or have messaging privacy settings allowing this
    is_friend = Friendship.objects.filter(
        Q(sender=user_profile.user, receiver=request.user, status='accepted') |
        Q(sender=request.user, receiver=user_profile.user, status='accepted')
    ).exists()
    
    if not is_friend and user_profile.message_privacy != 'everyone':
        messages.error(request, "You cannot message this user.")
        return redirect('social:dashboard')
    
    # Fetch messages between the users
    messages_between_users = Message.objects.filter(
        Q(sender=request.user, receiver=user_profile.user) |
        Q(sender=user_profile.user, receiver=request.user)
    ).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            
            # Create a new message
            message = Message(sender=request.user, receiver=user_profile.user, content=content)
            message.save()
            
            messages.success(request, "Message sent successfully.")
            return redirect('social:message_thread', username=username)  # Redirect back to the message thread
    
    else:
        form = MessageForm()
    
    return render(request, 'social/message_thread.html', {
        'user_profile': user_profile,
        'messages_between_users': messages_between_users,
        'form': form,
    })

def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id, receiver=request.user)
    
    if request.method == 'POST':
        message.delete()
        # Optionally, you can add a success message here
        return redirect('social:messaging')
    
    return render(request, 'social/delete_message.html', {'message': message})

@login_required
def delete_all_messages(request):
    if request.method == 'POST':
        # Delete all messages for the current user
        Message.objects.filter(receiver=request.user).delete()
        # Optionally, you can add a success message here
        return redirect('social:messaging')
    
    return render(request, 'social/delete_all_messages.html')