from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from user_app.models import User

ROLE_GROUP_MAPPING = {
    'administrator': 'Administrator',
    'hr': 'HR',
    'staff': 'Staff',
}

@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    # Clear existing groups to avoid conflicts
    instance.groups.clear()
    
    print(f"Instance {instance}")

    # Get the group name from the role
    group_name = ROLE_GROUP_MAPPING.get(instance.role)

    if group_name:
        # Get or create the group
        group, created = Group.objects.get_or_create(name=group_name)

        # Add the user to the group
        instance.groups.add(group)