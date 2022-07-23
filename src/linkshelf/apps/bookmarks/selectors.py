import logging
from typing import Iterable, Optional

from django.db.models import Count

from linkshelf.apps.bookmarks.models import Bookmark, Tag

logger = logging.getLogger(__name__)


def get_all_bookmarks(*, filters: Optional[dict] = None) -> Iterable[Bookmark]:
    """ """
    if filters:
        if tag_names := filters.get('tags'):
            return get_bookmarks_with_given_tags(tag_names=tag_names)
    return Bookmark.objects.all()


def get_all_tags() -> Iterable[Tag]:
    """ """
    return Tag.objects.all()


def get_bookmarks_with_given_tags(*, tag_names: list[str]) -> Iterable[Bookmark]:
    """ """
    return Bookmark.objects.filter(
        tags__in=tag_names
    ).annotate(
        num_tags=Count('tags')
    ).filter(
        num_tags=len(tag_names)
    )
