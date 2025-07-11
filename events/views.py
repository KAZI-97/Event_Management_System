from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from .models import Event, Category
from .forms import EventForm, CategoryForm
from datetime import date
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def group_required(group_name):
    def check(user):
        if not user.is_authenticated:
            return False  # Let login_required handle it
        if user.is_superuser or user.groups.filter(name=group_name).exists():
            return True
        raise PermissionDenied 
    return check 

admin_required = group_required('Admin')
organizer_required = group_required('Organizer')
participant_required = group_required('Participant')




def event_list(request):
    query = request.GET.get('q', '')
    events = Event.objects.select_related('category').prefetch_related('rsvped_users').all()

    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    return render(request, 'events/event_list.html', {'events': events, 'query': query})

def event_detail(request, pk):
    event_obj = get_object_or_404(
        Event.objects.prefetch_related('rsvped_users').select_related('category'),
        pk=pk
    )
    return render(request, 'events/event_details.html', {'event': event_obj})

# Event create
@login_required
@user_passes_test(group_required('Organizer')) 
def event_create(request):
    form = EventForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Add Event'})

# Event edit
@login_required
@user_passes_test(group_required('Organizer'))
def event_edit(request, pk):
    event_obj = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None,request.FILES or None, instance=event_obj)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Edit Event'})

# Event delete
@login_required
@user_passes_test(group_required('Organizer'))
def event_delete(request, pk):
    if not request.user.has_perm('events.delete_event'):
        return HttpResponse("You do not have permission to perform this action.", status=403)
    event_obj = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event_obj.delete()
        return redirect('event-list')
    return render(request, 'events/object_delete.html', {'object': event_obj})

# Category views (list, create, edit, delete)
@login_required
@user_passes_test(group_required('Organizer'))
def category_list(request):
    categories = Category.objects.annotate(event_count=Count('event')).all()
    return render(request, 'events/category_list.html', {'categories': categories})

@login_required
@user_passes_test(group_required('Organizer'))
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Add Category'})

@login_required
@user_passes_test(group_required('Organizer'))
def category_edit(request, pk):
    category_obj = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category_obj)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
@user_passes_test(group_required('Organizer'))
def category_delete(request, pk):
    category_obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_obj.delete()
        return redirect('category-list')
    return render(request, 'events/object_delete.html', {'object': category_obj})

# Participant views (list, create, edit, delete)
# @login_required
# @admin_required
# def participant_list(request):
#     participants = Participant.objects.prefetch_related('events').all()
#     return render(request, 'events/participant_list.html', {'participants': participants})

# @login_required
# @admin_required
# def participant_create(request):
#     form = ParticipantForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('participant-list')
#     return render(request, 'events/object_form.html', {'form': form, 'title': 'Add Participant'})

# @login_required
# @admin_required
# def participant_edit(request, pk):
#     participant_obj = get_object_or_404(Participant, pk=pk)
#     form = ParticipantForm(request.POST or None, instance=participant_obj)
#     if form.is_valid():
#         form.save()
#         return redirect('participant-list')
#     return render(request, 'events/object_form.html', {'form': form, 'title': 'Edit Participant'})

# @login_required
# @admin_required
# def participant_delete(request, pk):
#     participant_obj = get_object_or_404(Participant, pk=pk)
#     if request.method == 'POST':
#         participant_obj.delete()
#         return redirect('participant-list')
#     return render(request, 'events/object_confirm_delete.html', {'object': participant_obj})
@login_required
@user_passes_test(group_required('Admin'))
def participant_list(request):
    participants = User.objects.filter(groups__name='Participant')
    return render(request, 'events/participant_list.html', {'participants': participants})



@login_required
@user_passes_test(group_required('Organizer'))
def organizer_dashboard(request):
    today = timezone.now().date()

    total_events = Event.objects.count()
    # total_participants = Participant.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        # 'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
        'all_events': Event.objects.all(),
        'today': today,
    })
def home(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')
    return render(request, "events/home.html", {"events": upcoming_events})
@login_required
@user_passes_test(group_required('Admin'))
def admin_dashboard(request):
    total_events = Event.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    total_participants = User.objects.filter(groups__name='Participant').count()

    context = {
        'total_events': total_events,
        'total_users': total_users,
        'total_categories': total_categories,
        'total_participants': total_participants,
    }
    return render(request, 'events/dashboards/admin_dashboard.html', context)


@login_required
@user_passes_test(group_required('Participant'))
def participant_dashboard(request):
    user = request.user
    rsvp_events = user.rsvp_events.all() 

    context = {
        'rsvp_events': rsvp_events,
    }
    return render(request, 'events/dashboards/participant_dashboard.html', context)

def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.rsvped_users.all():
        event.rsvped_users.remove(user)
        messages.success(request, f"You have cancelled your RSVP for {event.name}.")
    else:
        event.rsvped_users.add(user)
        messages.success(request, f"You have successfully RSVP’d to {event.name}.")
    try:
        send_mail(
                subject="RSVP Confirmation",
                message=f"Hi {user.first_name},\n\nYou have successfully RSVP'd to the event: {event.name}.\n\nDate: {event.date}\nTime: {event.time}\nLocation: {event.location}\n\nThank you!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
    except Exception as e:
            print(f"Failed to send RSVP email: {e}")

    return redirect('event-detail', pk=event_id)
