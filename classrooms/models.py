from django.db import models
from django.conf import settings
from institutions.models import Institution
from products.models import Product
from members.models import BaseMember, BaseMemberType
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_currentuser.middleware import get_current_authenticated_user


class Classroom(Product):
    code = models.CharField(max_length=8, unique=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)

    # Hack to pass the user to post save signal.
    def save(self, *args, **kwargs):
        # Hack to pass the user to post save signal.
        self.current_authenticated_user = get_current_authenticated_user()
        super(Classroom, self).save(*args, **kwargs)


class ClassroomMember(BaseMember):
    options = (("adviser", "Adviser"), ("student", "Student"))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=10, choices=options, default="student")

    class Meta:
        unique_together = ["user", "classroom"]

    def __str__(self):
        return "%s - %s" % (self.user.full_name, self.classroom.name)


# signals
@receiver(post_save, sender=Classroom)
def classroom_create_owner(created, instance, *args, **kwargs):

    if created:
        user = getattr(instance, "current_authenticated_user", None)
        print(user)

        defaultMember = ClassroomMember.objects.create(classroom=instance, role="adviser", user=user)
        defaultMember.save()
