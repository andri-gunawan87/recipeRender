from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("recipe/<int:recipe_id>", views.detail, name="detail"),
    path("favorite", views.favorite, name="favorite"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("addcomment", views.addcomment, name="addcomment"),
    path("search/", views.search, name="search"),
    path("like/<int:post_id>", views.like, name="like"),
    path("all_recipe", views.all_recipe, name="all_recipe"),
    path("new_recipe", views.new_recipe, name="new_recipe")
]
