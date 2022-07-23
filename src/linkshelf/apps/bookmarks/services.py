import logging

from linkshelf.apps.bookmarks.models import Bookmark, Tag


logger = logging.getLogger(__name__)

# __all__ = []


class ServiceError(Exception):
    pass


def create_bookmark(*, url: str) -> Bookmark:
    """ """
    bookmark = Bookmark(url=url)
    bookmark.full_clean()
    bookmark.save()
    logger.debug('Bookmark created.')
    return bookmark


def create_tag(*, name: str) -> Tag:
    """ """
    tag = Tag(name=name)
    tag.full_clean()
    tag.save()
    logger.debug('Tag created.')
    return tag


def assign_tag_to_bookmark(*, bookmark_id: int, tag_name: str) -> Bookmark:
    bookmark = Bookmark.objects.get(id=bookmark_id)
    tag = Tag.objects.get(name=tag_name)
    bookmark.tags.add(tag)
    logger.debug(f'Tag with name: {tag_name} assigned to bookmark with id: {bookmark_id}.')
    return bookmark
