from django.contrib import admin
from django.db.utils import ProgrammingError
from .models import Video_products, Polygraphy, Work_in_elections, Settings
    
class Video_productsAdmin(admin.ModelAdmin):
    ordering = ['title', ]
    search_fields = ['title', ]  

class PolygraphyAdmin(admin.ModelAdmin):
    ordering = ['title', ]
    search_fields = ['title', ]  
    
class Work_in_electionsAdmin(admin.ModelAdmin):
    ordering = ['title', ]
    search_fields = ['title', ]  

class SettingsAdmin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            Settings.load().save()
        except ProgrammingError:
            pass
 
    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False
 
    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False
 
 
admin.site.register(Video_products, Video_productsAdmin)
admin.site.register(Polygraphy, PolygraphyAdmin)
admin.site.register(Work_in_elections, Work_in_electionsAdmin)
admin.site.register(Settings, SettingsAdmin)