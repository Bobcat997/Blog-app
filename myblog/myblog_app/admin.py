from django.contrib import admin
from .models import Comment, Entry

myModels = [Comment, Entry]
admin.site.register(myModels)