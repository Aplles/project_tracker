# -*- coding: utf8 -*-
from django.db import models


class FileField(models.FileField):
    def save_form_data(self, instance, data):
        if data is not None:
            file = getattr(instance, self.attname)
            if file != data:
                file.delete(save=False)
        super().save_form_data(instance, data)


class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    file = FileField(
        "Файл",
        upload_to='documents/',
        null=True,
        blank=True,
        max_length=1023,
    )
    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиция",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='documents_task',
        verbose_name='Задача'
    )

    def __str__(self):
        return self.name[0:50]

    class Meta:
        ordering = ["position"]
        db_table = "documents"
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
