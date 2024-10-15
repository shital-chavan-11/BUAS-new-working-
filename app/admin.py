from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email','date_of_birth','gender',)



admin.site.register(CustomUser, CustomUserAdmin)




