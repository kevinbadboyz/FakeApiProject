from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    is_admin = models.BooleanField(default = False)    

    def __str__(self):
        return str(self.username) + ' ' + str(self.first_name) + ' ' + str(self.last_name)

class Todo(models.Model):
    title = models.CharField(max_length = 200)
    completed = models.BooleanField(default = False)
    user_create = models.ForeignKey(User, related_name = 'user_create_todo', blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_todo', blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField(max_length = 200)
    body = models.TextField()
    user_create = models.ForeignKey(User, related_name = 'user_create_post', blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_post', blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title