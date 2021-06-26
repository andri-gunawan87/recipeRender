from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="mail_index"),
    path("login", views.login_view, name="mail_login"),
    path("logout", views.logout_view, name="mail_logout"),
    path("register", views.register, name="mail_register"),

    # API Routes
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
]
