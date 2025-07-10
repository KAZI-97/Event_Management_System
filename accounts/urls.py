from django.urls import path
from . import views

urlpatterns = [
    path("sign-up/", views.sign_up, name="sign-up"),
    path("sign-in/", views.sign_in, name="sign-in"),  # ← change from "login/"
    path("sign-out/", views.sign_out, name="sign-out"),  # ← change from "logout/"
    path("activate/<int:user_id>/<str:token>/", views.activate_user, name="activate-user"),
]
