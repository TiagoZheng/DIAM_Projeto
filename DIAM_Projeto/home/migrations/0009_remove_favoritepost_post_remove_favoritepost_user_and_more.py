# Generated by Django 4.2.1 on 2023-05-13 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_customuser_favoritepost_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritepost',
            name='post',
        ),
        migrations.RemoveField(
            model_name='favoritepost',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='FavoritePost',
        ),
    ]