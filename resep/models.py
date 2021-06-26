from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.TextField()
    key = models.CharField(max_length = 128)
    image = models.URLField()
    difficulty = models.CharField(max_length = 64)
    times = models.CharField(max_length = 64)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    desc = models.TextField()
    ingredient = models.JSONField()
    step = models.JSONField()
    like_count = models.IntegerField(default=0)
    
    def serialize(self):
        return {
            "id": self.id,
            "like": self.like_count,
        }
class Likes(models.Model):
    user = user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    rec = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="like")
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_fav")
    rec = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorite")
    fav = models.BooleanField(default=False)    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    rec = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comment")
    time = models.DateTimeField(auto_now_add=True, blank=True)
    comment = models.CharField(max_length = 200)