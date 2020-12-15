from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import *

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="Agent")
        instance.groups.add(group)

        team = Team.objects.get(team_name="Training")

        Agent.objects.create(
            user=instance,
            team_id=team
        )

post_save.connect(customer_profile, sender=User)
