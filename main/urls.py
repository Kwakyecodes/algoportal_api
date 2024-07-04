from django.urls import path

from . import views


urlpatterns = [
    path('fetch-code/', views.fetch_code),
    path('fetch-debugger/', views.fetch_debugger),
]