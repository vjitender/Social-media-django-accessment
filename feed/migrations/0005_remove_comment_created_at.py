# Generated by Django 4.2.5 on 2023-09-23 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_alter_comment_post_alter_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created_at',
        ),
    ]
