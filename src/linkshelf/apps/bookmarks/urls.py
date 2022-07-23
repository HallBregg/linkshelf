from django.urls import path

from linkshelf.apps.bookmarks import views

urlpatterns = [
    path('test', views.ListBookmarksView.as_view()),

    path('bookmarks', views.ListBookmarks.as_view(), name='bookmarks-list'),
]
