from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .forms import PropertyFilterForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')


def property_list(request):
    # Fetch all properties
    properties = Property.objects.all()

    # Create an instance of the filter form
    filter_form = PropertyFilterForm(request.GET)

    # Process the filter form data
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    property_type = request.GET.get('property_type')
    location = request.GET.get('location')

    # Apply filters based on the provided parameters
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if location:
        properties = properties.filter(city=location)
    if property_type:
        properties = properties.filter(property_type=property_type)

    context = {
        'properties': properties,
        'filter_form': filter_form,
    }

    return render(request, 'myapp/property_list.html', context)

def property_filter(request):
    # Create an instance of the filter form
    filter_form = PropertyFilterForm(request.GET)

    context = {
        'filter_form': filter_form,
    }

    return render(request, 'myapp/filter.html', context)


def property_detail(request, property_id ):
    propertyy = get_object_or_404(Property, id=property_id)
    return render(request, 'myapp/property_detail.html', {'property': propertyy})


@login_required
def agent_detail(request, agent_id):
    agent = get_object_or_404(AgentProfile, id=agent_id)
    properties = Property.objects.filter(agent=agent.user)
    return render(request, 'myapp/agent_detail.html', {'agent': agent, 'properties': properties})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = addnewproperty(request.POST, request.FILES)
        if form.is_valid():
            # Save the property or perform other actions
            form.save()
            return redirect('myapp:home')
    else:
        form = addnewproperty()  # Initialize the form for GET request
    return render(request, 'myapp/addnewproperty.html', {'form': form})

@login_required
def property_delete(request , property_id):
    propertyy = get_object_or_404(Property, id=property_id)
    if request.user == propertyy.agent or request.user.is_superuser:
        propertyy.delete()
    # propertees = Property.objects.all()
    # # return render(request, 'myapp/home.html',{'propertees': propertees})
        return redirect('myapp:home')
    else:
        # You can handle unauthorized deletion here (e.g., show a message)
        return render(request, 'myapp/unknown_delete.html')



    
    
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST , request.FILES)
        if form.is_valid():
            print(f"name is : {form.cleaned_data['name']}")
            print(f"Email is : {form.cleaned_data['email']}")
            print(f"Message is : {form.cleaned_data['message']}")
            return redirect('myapp:contact')
    else:
        form = ContactForm()        
    return render(request , 'myapp/contact.html'  , {'form' : form})

def about(request):
    return render(request , 'myapp/about.html')


@login_required
def agent_create(request):
    if request.method == 'POST':
        form = addnewagent(request.POST, request.FILES)
        if form.is_valid():
            # Save the property or perform other actions
            form.save()
            return redirect('myapp:home')
    else:
        form = addnewagent()  # Initialize the form for GET request
    return render(request, 'myapp/addnewagent.html', {'form': form})


def Delete_account(requsest):
    requsest.user.delete()
    messages.success(requsest , "Your account has been deleted!")
    return redirect('myapp:home')