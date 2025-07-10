from django.urls import path
# user/urls.py
from django.urls import path
from .views import sign_up, activate_user, sign_in, sign_out

urlpatterns = [
    path('register/', sign_up, name='sign-up'),
    path('login/', sign_in, name='sign-in'),     # custom sign in
    path('logout/', sign_out, name='sign-out'),  # custom logout
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
]
