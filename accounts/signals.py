from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomUser, StudentProfile, TeacherProfile, AdminProfile
from datetime import date

@receiver(post_save, sender=CustomUser)
def create_profile_based_on_role(sender, instance, created, **kwargs):
    if created:
        if instance.role == "student":
            StudentProfile.objects.create(
                user=instance,
                roll=f"R{instance.id}",
                course="Not Assigned",
                year=date.today().year,
                section="A"
            )
        elif instance.role == "teacher":
            TeacherProfile.objects.create(
                user=instance,
                subject="Not Assigned",
                department="Not Assigned",
                designation="Not Assigned"
            )
        elif instance.role == "admin":
            AdminProfile.objects.create(
                user=instance,
                office="Main Office",
                position="Staff"
            )

@receiver(post_delete, sender=CustomUser)
def delete_profile_when_user_deleted(sender, instance, **kwargs):
    try:
        if instance.role == "student":
            StudentProfile.objects.filter(user=instance).delete()
        elif instance.role == "teacher":
            TeacherProfile.objects.filter(user=instance).delete()
        elif instance.role == "admin":
            AdminProfile.objects.filter(user=instance).delete()
    except Exception as e:
        print("Profile deletion error:", e)