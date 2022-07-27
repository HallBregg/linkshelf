from django.shortcuts import resolve_url
from django.test import TestCase
from rest_framework.test import APIClient

from linkshelf.apps.bookmarks.models import Bookmark, Tag


class TestListBookmarksView(TestCase):
    def test_get_empty(self):
        client = APIClient()
        response = client.get(resolve_url('bookmarks-list'))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'next': None, 'previous': None, 'results': []})

    def test_get_bookmarks_without_tags(self):
        initial_object = Bookmark.objects.create(url='https://google.com')
        client = APIClient()
        response = client.get(resolve_url('bookmarks-list'))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': str(initial_object.id),
                        'url': initial_object.url,
                        'created_at': initial_object.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        'tags': []
                    }
                ]}
        )

    def test_get_bookmarks_with_tags(self):
        initial_object = Bookmark.objects.create(url='https://google.com')
        tag_one = Tag.objects.create(name='tag_one')
        tag_two = Tag.objects.create(name='tag_two')
        initial_object.tags.add(tag_one, tag_two)

        client = APIClient()
        response = client.get(resolve_url('bookmarks-list'))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': str(initial_object.id),
                        'url': initial_object.url,
                        'created_at': initial_object.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        'tags': ['tag_one', 'tag_two']
                    }
                ]}
        )

    def test_get_bookmarks_with_tags_filter_non_existing(self):
        initial_object = Bookmark.objects.create(url='https://google.com')
        tag_one = Tag.objects.create(name='tag_one')
        tag_two = Tag.objects.create(name='tag_two')
        initial_object.tags.add(tag_one, tag_two)

        client = APIClient()
        response = client.get(resolve_url('bookmarks-list'), data={'tags': 'tag_three'})
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'next': None,
                'previous': None,
                'results': []}
        )

    def test_get_bookmarks_with_tags_filter(self):
        bookmark1 = Bookmark.objects.create(url='https://google1.com')
        bookmark2 = Bookmark.objects.create(url='https://google2.com')
        tag_one = Tag.objects.create(name='tag_one')
        tag_two = Tag.objects.create(name='tag_two')
        bookmark1.tags.add(tag_one, tag_two)
        bookmark2.tags.add(tag_one)

        client = APIClient()
        response = client.get(resolve_url('bookmarks-list'), data={'tags': 'tag_one,tag_two'})
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': str(bookmark1.id),
                        'url': bookmark1.url,
                        'created_at': bookmark1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        'tags': ['tag_one', 'tag_two']
                    }
                ]}
        )

    def test_get_bookmarks_with_tags_filter_(self):
        bookmark1 = Bookmark.objects.create(url='https://google1.com')
        bookmark2 = Bookmark.objects.create(url='https://google2.com')
        tag_one = Tag.objects.create(name='tag_one')
        tag_two = Tag.objects.create(name='tag_two')
        bookmark1.tags.add(tag_one, tag_two)
        bookmark2.tags.add(tag_one)

        client = APIClient()
        response = client.get(resolve_url('bookmarks-list'), data={'tags': 'tag_one'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(
            {
                'id': str(bookmark1.id),
                'url': bookmark1.url,
                'created_at': bookmark1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'tags': ['tag_one', 'tag_two']
            },
            data['results']
        )
        self.assertIn(
            {
                'id': str(bookmark2.id),
                'url': bookmark2.url,
                'created_at': bookmark2.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'tags': ['tag_one']
            },
            data['results']
        )


class TestListTagsView(TestCase):
    def test_get_empty_list(self):
        client = APIClient()
        response = client.get(resolve_url('tags-list'))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'next': None, 'previous': None, 'results': []})

    def test_get_one(self):
        tag_one = Tag.objects.create(name='tag_one')
        tag_two = Tag.objects.create(name='tag_two')

        client = APIClient()
        response = client.get(resolve_url('tags-list'))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            {
                'name': 'tag_one',
                'created_at': tag_one.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
            data['results']
        )
        self.assertIn(
            {
                'name': 'tag_two',
                'created_at': tag_two.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
            data['results']
        )


class TestAssignTagToBookmark(TestCase):
    def test_one(self):
        client = APIClient()
        response = client.get(resolve_url('tags-list', bookmark_id=1, tag_id='git'))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'bookmark_id': 1, 'tag_id': 'git'})
