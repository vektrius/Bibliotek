from django.contrib import admin

# Register your models here.
from .models import Account, Book, Genre, Rate

admin.site.register(Account)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Rate)