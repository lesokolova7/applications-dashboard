from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(tf_urls)),
    path("", include("user_sessions.urls", "user_sessions")),
    path("", include("main.urls")),
    path("account/", include("account.urls", namespace="account")),
    path("__reload__/", include("django_browser_reload.urls")),
]
