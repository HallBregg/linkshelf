from django.urls import path

from linkshelf.apps.bookmarks import views

urlpatterns = [
    path(
        'test',
        views.ListBookmarksView.as_view()
    ),
    path(
        'bookmarks',
        views.ListBookmarks.as_view(),
        name='bookmarks-list'
    ),
    path(
        'bookmarks/<int:bookmark_id>/tags/<str:tag_id>',
        views.AddTagToBookmarkView.as_view(),
        name='bookmarks-tags-assign'
    ),
    path(
        'tags',
        views.ListTags.as_view(),
        name='tags-list'
    ),
]
