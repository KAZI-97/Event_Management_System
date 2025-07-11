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

organizer_required = user_passes_test(lambda u: u.groups.filter(name='Organizer').exists())
admin_required = user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
participant_required = user_passes_test(lambda u: u.groups.filter(name='Participant').exists())

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
                    return redirect('manager-dashboard')
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

