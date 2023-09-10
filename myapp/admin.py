from django.contrib import admin
from .models import *
# Register your models here.

class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name' ,)

class PropertyStatusAdmin(admin.ModelAdmin):
    list_display = ('name' ,)



class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title' , 'price' , 'city','agent')
    list_display_links = ('title' , 'city' , 'agent' ,)

class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user' , 'contact_number' ,)
    list_display_links = ('user' ,'contact_number' ,)

admin.site.register(City ,CityAdmin)
admin.site.register(PropertyType ,PropertyTypeAdmin)
admin.site.register(PropertyStatus ,PropertyStatusAdmin)
admin.site.register(AgentProfile ,AgentProfileAdmin)
admin.site.register(Property ,PropertyAdmin)
