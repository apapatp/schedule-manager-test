# Generated by Django 4.2 on 2024-10-17 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='end_time',
            new_name='start',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='start_time',
            new_name='stop',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='badge_ids',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='camera_ids',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
