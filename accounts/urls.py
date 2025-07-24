from django.urls import path
from accounts.views import sign_in,sign_out,sign_up,activate_user,SignUpView,SignOutView,ProfileView,EditProfileView,ChangePasswordView,CustomPasswordResetView,CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeDoneView
urlpatterns = [
    # path("sign-up/", sign_up, name="sign-up"),
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    # path("sign-out/", sign_out, name="sign-out"),
    path("sign-out/", SignOutView.as_view(), name="sign-out"),
    path("activate/<int:user_id>/<str:token>/",activate_user, name="activate-user"),
    path('profile/',ProfileView.as_view(template_name='accounts/profile.html'),name='profile'),
    path('password-change',ChangePasswordView.as_view(template_name='accounts/password_change.html'),name='password_change'),
    path('password-change/done',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    path('password-reset/',CustomPasswordResetView.as_view(),name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(),name='edit_profile'),
    # path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset')


]
