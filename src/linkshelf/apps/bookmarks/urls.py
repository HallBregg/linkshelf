from django.contrib import admin
from django.urls import path

from linkshelf.apps.bookmarks.views import test

urlpatterns = [
    path('', test, name='test'),
]
