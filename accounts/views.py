from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.forms import CustomRegistrationForm 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from accounts.forms import CustomRegistrationForm, EditProfileForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm

organizer_required = user_passes_test(lambda u: u.groups.filter(name='Organizer').exists())
admin_required = user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
participant_required = user_passes_test(lambda u: u.groups.filter(name='Participant').exists())

User = get_user_model()
# def sign_up(request):
#     if request.method == 'GET':
#         form = CustomRegistrationForm()
#         return render(request, "registration/register.html", {'form': form})
    
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password1'))
#             user.is_active = False
#             user.save()

#             participant_group = Group.objects.get(name='Participant')
#             user.groups.add(participant_group)

#             # Send account activation email
#             current_site = get_current_site(request)
#             subject = 'Activate Your Account'
#             message = render_to_string('registration/activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'user_id': user.id,
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(subject, message, to=[to_email])
#             email.send()

#     return render(request, "registration/register.html", {'form': form})


def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
        return render(request, "registration/register.html", {'form': form})

    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            participant_group = Group.objects.get(name='Participant')
            user.groups.add(participant_group)

            messages.success(request, "Account created! Please check your email to activate your account.")
            return redirect('sign-in')
    return render(request, "registration/register.html", {'form': form})


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account is now activated. You can log in.')
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid activation link.')
    except User.DoesNotExist:
        return HttpResponse('User not found.')
    
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name='Admin').exists():
                    return redirect('admin-dashboard')
                elif user.groups.filter(name='Organizer').exists():
                    return redirect('organizer-dashboard')
                elif user.groups.filter(name='Participant').exists():
                    return redirect('participant-dashboard')
                else:
                    return redirect('home') 
            else:
                messages.error(request, "Account inactive. Please activate via email.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'registration/login.html')


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('sign-in')

# Creating Class Base View from Here
"""
class SignUpView(View):
    def get(self, request):
        form = CustomRegistrationForm()
        return render(request, "registration/register.html", {'form': form})

    def post(self, request):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()


            participant_group = Group.objects.get(name='Participant')
            user.groups.add(participant_group)

            messages.success(request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')
        return render(request, "registration/register.html", {'form': form})
"""
class SignUpView(View):
    def get(self, request):
        form = CustomRegistrationForm()
        return render(request, "registration/register.html", {'form': form})

    def post(self, request):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()

            participant_group = Group.objects.get(name='Participant')
            user.groups.add(participant_group)

            # Send activation email
            current_site = get_current_site(request)
            subject = 'Activate Your Event Manager Account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'user_id': user.id,
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()

            messages.success(request, 'A confirmation mail sent. Please check your email')
            return redirect('sign-in')
        return render(request, "registration/register.html", {'form': form})
@method_decorator(login_required, name='dispatch')
class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('sign-in')
    
# Creating New View from Here
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['phone_number'] = user.phone_number
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')

class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully!")
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def form_valid(self, form):
        messages.success(self.request, "A reset email has been sent. Please check your inbox.")
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, "Password reset successfully!")
        return super().form_valid(form)