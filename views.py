# views.py

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["GET"])
def github_auth_redirect(request):
    redirect_uri = "http://localhost:5173/github/callback"
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={redirect_uri}&scope=user"
    return Response({"url": github_auth_url})


@api_view(["GET"])
def github_authenticate(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
    }
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data=data,
        headers={"Accept": "application/json"},
    )
    access_token = response.json().get("access_token")

    if access_token:
        user_data = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"},
        ).json()

        github_username = user_data.get("login")

        try:
            if User.objects.filter(username=github_username).exists():
                user = User.objects.get(username=github_username)
                token = get_tokens_for_user(user)
                return JsonResponse(token)

            github_email = user_data.get("email") if user_data.get("email") else ""
            first_name = (
                user_data.get("name", "").split()[0] if user_data.get("name") else ""
            )
            last_name = (
                user_data.get("name", "").split()[1] if user_data.get("name") else ""
            )
            # Assuming password generation for the new user
            password = user_data.get("node_id")

            user = User.objects.create_user(
                email=github_email,
                username=github_username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            token = get_tokens_for_user(user)
            return JsonResponse(token)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        return JsonResponse({"error": "Failed to authenticate with GitHub"}, status=400)


@api_view(["GET"])
def google_auth_redirect(request):
    redirect_uri = "http://localhost:8000/google/authenticate/"
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&scope=email%20profile&response_type=code"
    return Response({"url": google_auth_url})


@api_view(["GET"])
def google_authenticate(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://localhost:8000/google/authenticate/",
        "grant_type": "authorization_code",
    }

    # Exchange authorization code for access token
    response = requests.post("https://oauth2.googleapis.com/token", data=data)
    access_token = response.json().get("access_token")

    if access_token:
        # Fetch user data using access token from Google API
        user_data = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

        print(user_data)

        # Handle user creation or login logic here based on user_data

        return JsonResponse({"access_token": access_token})
    else:
        return JsonResponse({"error": "Failed to authenticate with Google"}, status=400)
