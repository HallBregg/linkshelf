# Generated by Django 4.0.6 on 2022-07-22 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_rename_bookmarks_bookmark_rename_tags_tag'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='bookmark',
            table='bookmark',
        ),
        migrations.AlterModelTable(
            name='tag',
            table='tag',
        ),
    ]
