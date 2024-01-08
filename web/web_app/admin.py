from django.contrib import admin
from web_app.models import (
    User, Todo, Post
)

admin.site.register(User)
admin.site.register(Todo)
admin.site.register(Post)
