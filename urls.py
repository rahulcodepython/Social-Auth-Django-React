from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    path("admin/", admin.site.urls),
] + [
    path("github/auth/", views.github_auth_redirect, name="github_auth_redirect"),
    path("github/authenticate/", views.github_authenticate, name="github_authenticate"),
    path("google/auth/", views.google_auth_redirect, name="google_auth_redirect"),
    path("google/authenticate/", views.google_authenticate, name="google_authenticate"),
]
