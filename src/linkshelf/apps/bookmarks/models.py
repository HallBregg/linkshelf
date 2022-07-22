from django.db import models


class Tag(models.Model):
    name = models.TextField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tag'


class Bookmark(models.Model):
    url = models.URLField(unique=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmark'

"""
query = Tag.objects.get(name='python').bookmark_set.all() &
        Tag.objects.get(name='design patterns').bookmark_set.all()
'SELECT "bookmark"."id", "bookmark"."url", "bookmark"."created_at" FROM "bookmark" INNER JOIN "bookmark_tags" ON ("bookmark"."id" = "bookmark_tags"."bookmark_id") LEFT OUTER JOIN "bookmark_tags" T4 ON ("bookmark"."id" = T4."bookmark_id") WHERE ("bookmark_tags"."tag_id" = python AND T4."tag_id" = design patterns)'

'5 0 0 SEARCH TABLE bookmark_tags USING INDEX bookmarks_tags_tag_id_a46d34d9 (tag_id=?)\n12 0 0 SEARCH TABLE bookmark USING INTEGER PRIMARY KEY (rowid=?)\n15 0 0 SEARCH TABLE bookmark_tags AS T4 USING COVERING INDEX bookmarks_tags_bookmark_id_tag_id_284dd9c3_uniq (bookmark_id=? AND tag_id=?)'

"""

"""
query = Bookmark.objects.filter(
            tags__in=['python', 'design patterns']
        ).annotate(
            num_tags=Count('tags')
        ).filter(num_tags=2)
'SELECT "bookmark"."id", "bookmark"."url", "bookmark"."created_at", COUNT("bookmark_tags"."tag_id") AS "num_tags" FROM "bookmark" INNER JOIN "bookmark_tags" ON ("bookmark"."id" = "bookmark_tags"."bookmark_id") WHERE "bookmark_tags"."tag_id" IN (python, design patterns) GROUP BY "bookmark"."id", "bookmark"."url", "bookmark"."created_at" HAVING COUNT("bookmark_tags"."tag_id") = 2'

'8 0 0 SEARCH TABLE bookmark_tags USING INDEX bookmarks_tags_tag_id_a46d34d9 (tag_id=?)\n26 0 0 SEARCH TABLE bookmark USING INTEGER PRIMARY KEY (rowid=?)\n29 0 0 USE TEMP B-TREE FOR GROUP BY'
"""
