# Generated by Django 5.2.3 on 2025-07-11 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_profile_cv_profile_cv_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cv_text',
        ),
        migrations.AddField(
            model_name='profile',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='cvs/'),
        ),
    ]
