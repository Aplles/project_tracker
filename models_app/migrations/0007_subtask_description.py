# Generated by Django 4.0 on 2023-10-22 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0006_dashboard_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='description',
            field=models.TextField(default=1, verbose_name='Описание подзадачи'),
            preserve_default=False,
        ),
    ]
