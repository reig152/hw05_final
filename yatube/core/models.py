from django.db import models


class DateModel(models.Model):
    """Абстрактная модель для создания даты добавления"""
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        # указываем абстрактную модель
        abstract = True
