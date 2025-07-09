from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from accounts.forms import CustomRegistrationForm
from django.shortcuts import get_object_or_404

def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False  # Deactivate until email confirmed
            user.save()

            # Assign to Participant group
            group = Group.objects.get(name='Participant')
            user.groups.add(group)

            # Generate simple activation link
            activation_link = request.build_absolute_uri(
                reverse('simple-activate-account', kwargs={'user_id': user.id})
            )

            # Send email
            subject = "Activate your account"
            message = f"Hi {user.username},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nIf you didn't request this, ignore this email."
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )

            messages.success(request, 'A confirmation mail was sent. Please check your email.')
            return redirect('sign-in')
        else:
            print('Form is not valid')

    return render(request, "registration/register.html", {'form': form})

from django.shortcuts import get_object_or_404

def activate_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
    else:
        messages.info(request, "Your account is already active.")
    return redirect('sign-in')



