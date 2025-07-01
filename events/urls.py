from django.urls import path
from .views import (
    organizer_dashboard, event_create, event_list, event_detail, event_edit, event_delete,
    category_list, category_create, participant_list, participant_create,home,participant_delete,participant_edit,category_delete,category_edit
)

urlpatterns = [
    path('', home, name='home'),
    path("manager-dashboard/", organizer_dashboard, name="manager-dashboard"),
    path("event-create/", event_create, name="event-create"),
    path("event-list/", event_list, name="event-list"),
    path("event-detail/<int:pk>/", event_detail, name="event-detail"),
    path("event-edit/<int:pk>/", event_edit, name="event-edit"),
    path("event-delete/<int:pk>/", event_delete, name="event-delete"),

    path("category-list/", category_list, name="category-list"),
    path("category-create/", category_create, name="category-create"),
    path("category-edit/<int:pk>/", category_edit, name="category-edit"),
    path("category-delete/<int:pk>/", category_delete, name="category-delete"),

    path("participant-list/", participant_list, name="participant-list"),
    path("participant-create/", participant_create, name="participant-create"),
    path("participant-edit/<int:pk>/", participant_edit, name="participant-edit"),
    path("participant-delete/<int:pk>/", participant_delete, name="participant-delete"),

]
