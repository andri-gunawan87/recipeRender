from django.contrib.auth.models import User
import uuid
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(to="resep.User", on_delete=models.CASCADE, related_name="user_p")
    body = models.TextField()
    like_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='user_image', blank=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "like": self.like_count,
            "date": self.date.strftime("%b %d %Y, %I:%M %p")
        }
    
class Follow(models.Model):
    user = models.ForeignKey(to="resep.User", on_delete=models.CASCADE, related_name="user_f")
    following = models.ForeignKey(to="resep.User", on_delete=models.CASCADE, related_name="user_following")
    friend_request = models.BooleanField(default=False)
    
class Profile(models.Model):
    user = models.OneToOneField(to="resep.User", on_delete=models.CASCADE, related_name="user_a")
    user_avatar = models.ImageField(upload_to='user_avatar', blank=True)
    country = models.CharField(max_length = 64, blank=True)
    address = models.CharField(blank=True, max_length = 255)
    city = models.CharField(max_length = 64, blank=True)
    postcode = models.CharField(max_length = 64, blank=True)
    bio = models.TextField(blank=True)
    
class Sns_comments(models.Model):
    cid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to="resep.User", on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    