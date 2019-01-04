from django.contrib import admin
from .models import Application,Service

# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name','appok')
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'serviceok')
    pass