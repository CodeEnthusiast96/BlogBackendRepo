# Generated by Django 4.2.8 on 2023-12-05 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0002_alter_post_author_delete_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
