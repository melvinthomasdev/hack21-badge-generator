from django.contrib import admin

from .models import People
# Register your models here.

class PeopleAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(People, PeopleAdmin)