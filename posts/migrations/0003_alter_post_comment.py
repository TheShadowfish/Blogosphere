# Generated by Django 5.1.2 on 2024-10-22 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0001_initial"),
        ("posts", "0002_alter_post_author_alter_post_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="comment",
            field=models.ManyToManyField(
                help_text="Добавьте комментарии",
                to="comments.comment",
                verbose_name="Комментарии",
            ),
        ),
    ]
