from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display, name="display"),
    path("wiki/", views.entry_form, name="entry_form"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
]
