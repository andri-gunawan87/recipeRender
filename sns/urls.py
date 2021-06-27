
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="sns_index"),
    path("login", views.login_view, name="sns_login"),
    path("logout", views.logout_view, name="sns_logout"),
    path("register", views.register, name="sns_register"),
    path("allposts", views.all_posts, name="all_posts"),
    path("follow", views.follow, name="follow"),
    path("<int:user_id>", views.profil, name="profil"),
    path("post/<int:post_id>", views.post, name="post"),
    path("like/<int:post_id>", views.like, name="sns_like"),
    path("account", views.account, name="account"),
    path("friends/<int:user_id>", views.friends, name="sns_friends"),
    path("comments/<int:item_id>", views.comments, name="sns_comments")
]
