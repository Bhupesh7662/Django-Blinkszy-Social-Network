from django.contrib import admin
from .models import Post, Profile, Like, Following, Comment

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Following)
admin.site.register(Comment)
