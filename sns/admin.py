from django.contrib import admin

# Register your models here.
from .models import Post, Follow, Profile

# Register your models here.
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Profile)