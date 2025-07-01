from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from .models import Event, Category, Participant
from .forms import EventForm, CategoryForm, ParticipantForm
from datetime import date
from django.utils import timezone

def event_list(request):
    query = request.GET.get('q', '')
    events = Event.objects.select_related('category').prefetch_related('participant_set').all()

    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    return render(request, 'events/event_list.html', {'events': events, 'query': query})

def event_detail(request, pk):
    event_obj = get_object_or_404(
        Event.objects.prefetch_related('participant_set').select_related('category'),
        pk=pk
    )
    return render(request, 'events/event_details.html', {'event': event_obj})

# Event create
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Add Event'})

# Event edit
def event_edit(request, pk):
    event_obj = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event_obj)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Edit Event'})

# Event delete
def event_delete(request, pk):
    event_obj = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event_obj.delete()
        return redirect('event-list')
    return render(request, 'events/object_confirm_delete.html', {'object': event_obj})

# Category views (list, create, edit, delete)
def category_list(request):
    categories = Category.objects.annotate(event_count=Count('event')).all()
    return render(request, 'events/category_list.html', {'categories': categories})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Add Category'})

def category_edit(request, pk):
    category_obj = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category_obj)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Edit Category'})

def category_delete(request, pk):
    category_obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_obj.delete()
        return redirect('category-list')
    return render(request, 'events/object_confirm_delete.html', {'object': category_obj})

# Participant views (list, create, edit, delete)
def participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'events/participant_list.html', {'participants': participants})

def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('participant-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Add Participant'})

def participant_edit(request, pk):
    participant_obj = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(request.POST or None, instance=participant_obj)
    if form.is_valid():
        form.save()
        return redirect('participant-list')
    return render(request, 'events/object_form.html', {'form': form, 'title': 'Edit Participant'})

def participant_delete(request, pk):
    participant_obj = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant_obj.delete()
        return redirect('participant-list')
    return render(request, 'events/object_confirm_delete.html', {'object': participant_obj})

def organizer_dashboard(request):
    today = timezone.now().date()

    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        'total_participants': total_participants,
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
