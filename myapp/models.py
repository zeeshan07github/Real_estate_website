from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location=settings.MEDIA_ROOT)
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class PropertyStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(null=True , blank = True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area = models.IntegerField()  # in square feet
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(PropertyStatus, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null = True , blank= True)
    contact_number = models.CharField(max_length=15)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

