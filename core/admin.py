from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Movie)

class MovieListAdmin(admin.ModelAdmin):
     list_display = ('owner_user','movie')
admin.site.register(MovieList,MovieListAdmin)
     

admin.site.register(Profile)