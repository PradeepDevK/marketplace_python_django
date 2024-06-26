# Generated by Django 5.0.2 on 2024-06-05 15:57

from django.db import migrations, models
from django.conf import settings

def update_admin_log_user_reference(apps, schema_editor):
    # Get the models
    User = apps.get_model(settings.AUTH_USER_MODEL)
    LogEntry = apps.get_model('admin', 'LogEntry')

    # Set the related_name for the custom user model
    for log_entry in LogEntry.objects.all():
        try:
            custom_user = User.objects.get(pk=log_entry.user_id)
            log_entry.user = custom_user
            log_entry.save()
        except User.DoesNotExist:
            # Handle case where user does not exist
            log_entry.user = None
            log_entry.save()

class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('administrator', 'ADMINISTRATOR'), ('hr', 'HR'), ('staff', 'STAFF')], max_length=15),
        ),
    ]
