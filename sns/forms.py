from django import forms
from .models import Post, Follow, Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class PostForm (forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'image')
     
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('country', 'address', 'city', 'postcode', 'user_avatar', 'bio')