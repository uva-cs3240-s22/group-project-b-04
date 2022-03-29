# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import CustomUser

# @receiver(post_save, sender=User)
# def create_CustomUser(sender, instance, created, **kwargs):
#     if created:
#         CustomUser.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_CustomUser(sender, instance, **kwargs):
#     instance.CustomUser.save()