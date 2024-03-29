from django.contrib import admin
from django.urls import path
from api.views import (
    HabitListCreateView,
    HabitRetrieveUpdateDestroyView,
    RegisterView,
    LoginView,
    CurrentUserView,
    EffortListCreateView,
    EffortRetrieveUpdateDestroyView,
    EffortListByWeekView,
    LogoutView,
    EffortCompletionView,
    HabitPerformanceView,
    YearlyHabitPerformanceView,
    RecentCompletionsView,
    SiteConfigView,
    UserUpdateView,
    UserListView,
    TicketListCreateView,
    TicketRetrieveUpdateDestroyView,
    AnnouncementListCreateView,
    AnnouncementRetrieveUpdateDestroyView,
    TicketCreateView,
    UserTicketListView,
    FeatureListCreateView,
    FeatureRetrieveUpdateDestroyView,
    PublicFeatureListView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/features/", PublicFeatureListView.as_view()),
    path("api/site-config/", SiteConfigView.as_view()),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/user/", CurrentUserView.as_view(), name="current-user"),
    path("api/auth/logout/", LogoutView.as_view(), name="logout"),
    path("api/habits/", HabitListCreateView.as_view(), name="habit-list-create"),
    path(
        "api/habits/<int:pk>/",
        HabitRetrieveUpdateDestroyView.as_view(),
        name="habit-detail",
    ),
    path("api/efforts/", EffortListCreateView.as_view(), name="effort-list-create"),
    path(
        "api/efforts/<int:pk>/",
        EffortRetrieveUpdateDestroyView.as_view(),
        name="effort-detail",
    ),
    path("api/efforts/week/<int:week>/", EffortListByWeekView.as_view()),
    path(
        "api/completion/<int:week>/", EffortCompletionView.as_view(), name="completion"
    ),
    path(
        "api/completion/<int:week>/recent",
        RecentCompletionsView.as_view(),
        name="recent-completions",
    ),
    path(
        "api/performance/<int:habit_id>/",
        HabitPerformanceView.as_view(),
        name="performance",
    ),
    path(
        "api/performance/global/",
        YearlyHabitPerformanceView.as_view(),
        name="yearly-habit-performance",
    ),
    path("api/user/profile/", UserUpdateView.as_view(), name="user-update"),
    path("api/tickets/", UserTicketListView.as_view(), name="user-ticket-list"),
    path("api/tickets/create/", TicketCreateView.as_view(), name="ticket-create"),
    path("api/backoffice/users/", UserListView.as_view(), name="backoffice-user-list"),
    path(
        "api/backoffice/tickets/",
        TicketListCreateView.as_view(),
        name="ticket-list-create",
    ),
    path(
        "api/backoffice/tickets/<int:pk>/",
        TicketRetrieveUpdateDestroyView.as_view(),
        name="ticket-detail",
    ),
    path(
        "api/backoffice/announcements/",
        AnnouncementListCreateView.as_view(),
        name="announcement-list-create",
    ),
    path(
        "api/backoffice/announcements/<int:pk>/",
        AnnouncementRetrieveUpdateDestroyView.as_view(),
        name="announcement-detail",
    ),
    path(
        "api/backoffice/features/",
        FeatureListCreateView.as_view(),
        name="feature-list-create",
    ),
    path(
        "api/backoffice/features/<int:pk>/",
        FeatureRetrieveUpdateDestroyView.as_view(),
        name="feature-detail",
    ),
]
