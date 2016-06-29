from example.models import Citizen
from django.contrib import admin

# Register your models here.

class CitizenAdmin(admin.ModelAdmin):
    pass
admin.site.register(Citizen, CitizenAdmin)
