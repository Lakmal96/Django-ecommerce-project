# Generated by Django 3.1 on 2021-07-19 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_posts_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]