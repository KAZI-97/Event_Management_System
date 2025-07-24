from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from events.forms import StyledFormMixin
from accounts.models import CustomUser

User = get_user_model()

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','phone_number', 'password1', 'password2']

class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'profile_image']
class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("No active user is associated with this email address.")
        return email


class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass