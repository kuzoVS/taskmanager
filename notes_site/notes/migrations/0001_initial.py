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
            name="Note",
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
                ("title", models.CharField(max_length=100, verbose_name="Заголовок")),
                (
                    "body",
                    models.TextField(blank=True, max_length=1000, verbose_name="Текст"),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("yellow", "Жёлтый"),
                            ("pink", "Розовый"),
                            ("green", "Зелёный"),
                            ("blue", "Голубой"),
                            ("purple", "Фиолетовый"),
                        ],
                        default="yellow",
                        max_length=10,
                        verbose_name="Цвет",
                    ),
                ),
                (
                    "pinned",
                    models.BooleanField(default=False, verbose_name="Закреплена"),
                ),
                (
                    "archived",
                    models.BooleanField(default=False, verbose_name="В архиве"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создана"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-pinned", "-created_at"],
            },
        ),
    ]
