from django.conf import settings
from django.db import models


class Note(models.Model):
    COLORS = [
        ("yellow", "Жёлтый"),
        ("pink", "Розовый"),
        ("green", "Зелёный"),
        ("blue", "Голубой"),
        ("purple", "Фиолетовый"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="notes")
    title = models.CharField("Заголовок", max_length=100)
    body = models.TextField("Текст", max_length=1000, blank=True)
    color = models.CharField("Цвет", max_length=10, choices=COLORS, default="yellow")
    pinned = models.BooleanField("Закреплена", default=False)
    archived = models.BooleanField("В архиве", default=False)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        ordering = ["-pinned", "-created_at"]

    def __str__(self):
        return self.title
