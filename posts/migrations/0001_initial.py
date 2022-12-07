# Generated by Django 4.1.1 on 2022-10-17 12:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="제목")),
                ("content", models.TextField(max_length=400, verbose_name="내용")),
                ("views", models.PositiveIntegerField(default=0, verbose_name="조회수")),
                (
                    "created_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성시간"),
                ),
                (
                    "updated_date",
                    models.DateTimeField(auto_now=True, verbose_name="수정시간"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="활성화")),
            ],
        ),
        migrations.CreateModel(
            name="TagName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="해쉬태그")),
            ],
        ),
        migrations.CreateModel(
            name="PostTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "posts",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posts.post"
                    ),
                ),
                (
                    "tags",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posts.tagname"
                    ),
                ),
            ],
            options={
                "db_table": "posts_tags",
            },
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                related_name="tags",
                through="posts.PostTag",
                to="posts.tagname",
                verbose_name="해쉬태그",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="writer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="작성자",
            ),
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="posts.post",
                        verbose_name="게시글",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="사용자",
                    ),
                ),
            ],
        ),
    ]
