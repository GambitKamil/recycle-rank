from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, dashboard_view, add_entry_view

from .forms import StudentLoginForm
from .views import register_view, dashboard_view
from .views import (
    register_view,
    dashboard_view,
    add_entry_view,
    leaderboard_students_view,
    leaderboard_faculties_view,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="core/login.html",
            authentication_form=StudentLoginForm
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("add/", add_entry_view, name="add_entry"),
    path("leaderboard/", leaderboard_students_view, name="leaderboard_students"),
    path("faculties/", leaderboard_faculties_view, name="leaderboard_faculties"),

]
