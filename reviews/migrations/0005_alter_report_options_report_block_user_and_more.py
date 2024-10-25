# Generated by Django 5.1.2 on 2024-10-22 01:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_report'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='report',
            name='block_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='processed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='processed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_reports', to=settings.AUTH_USER_MODEL),
        ),
    ]
