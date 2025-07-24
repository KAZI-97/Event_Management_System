from django.urls import path
from events.views import(
    organizer_dashboard, event_create, event_list, event_detail, event_edit, event_delete,
    category_list, category_create,home,category_delete,category_edit,participant_list,admin_dashboard,participant_dashboard,rsvp_event,EventDetailView,CategoryListView,OrganizerDashboardView
)

urlpatterns = [
    path('', home, name='home'),
    # path("manager-dashboard/", organizer_dashboard, name="manager-dashboard"),
    path("organizer-dashboard/", OrganizerDashboardView.as_view(), name="organizer-dashboard"),
    path("event-create/", event_create, name="event-create"),
    path("event-list/", event_list, name="event-list"),
    # path("event-detail/<int:pk>/", event_detail, name="event-detail"),
    path("event-detail/<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("event-edit/<int:pk>/", event_edit, name="event-edit"),
    path("event-delete/<int:pk>/", event_delete, name="event-delete"),

    # path("category-list/", category_list, name="category-list"),
    path("category-list/", CategoryListView.as_view(), name="category-list"),
    path("category-create/", category_create, name="category-create"),
    path("category-edit/<int:pk>/", category_edit, name="category-edit"),
    path("category-delete/<int:pk>/", category_delete, name="category-delete"),
    path('participants/', participant_list, name='participant-list'),
    path('dashboards/admin/',admin_dashboard, name='admin-dashboard'),
    path('dashboard/participant/',participant_dashboard, name='participant-dashboard'),
    path('event/<int:event_id>/rsvp/',rsvp_event, name='rsvp-event'),


]
