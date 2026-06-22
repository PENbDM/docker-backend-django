from django.db import models
from django.conf import settings

class Company(models.Model):
    name=models.CharField(max_length=100,unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_companies"
    )
    # "Use whatever User model is configured in settings.py"
    created_at=models.DateTimeField(auto_now_add=True)

class CompanyMember(models.Model):
    ROLE_CHOICES = [
        ('owner','Owner'),
        ('manager','Manager'),
        ('analyst','Analyst'),
        ('viewer','Viewer'),]

    company=models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='member'
    )
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        #"Use whatever User model is configured in settings.py"
        on_delete=models.CASCADE,
        related_name='company_memberships'
    )

    role=models.CharField(max_length=100,choices=ROLE_CHOICES)
    joined_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "user")
        #The same user cannot be added to the same company twice.