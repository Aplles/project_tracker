# Generated by Django 4.0 on 2023-12-10 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0011_project_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('manager', 'Менеджер'), ('programmer', 'Программист')], default='programmer', max_length=50),
        ),
    ]
