from django.contrib import admin
from .models import Book, Todo

# Register the models with the admin site
admin.site.register(Book)
admin.site.register(Todo)