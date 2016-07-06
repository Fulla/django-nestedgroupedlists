from example.models import Citizen, CitizenExt
from django.contrib import admin

# Register your models here.

class CitizenAdmin(admin.ModelAdmin):
    pass
admin.site.register(Citizen, CitizenAdmin)

class CitizenExtAdmin(admin.ModelAdmin):
    pass
admin.site.register(CitizenExt, CitizenExtAdmin)
