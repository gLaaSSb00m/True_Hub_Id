from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProfileField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('date', 'Date'),
        ('select', 'Select'),
        ('email', 'Email'),
        ('number', 'Number'),
    ]

    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES, default='text')
    required = models.BooleanField(default=False)
    choices = models.TextField(blank=True, help_text="Comma-separated choices for select fields")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label

    def get_choices_list(self):
        if self.choices:
            return [choice.strip() for choice in self.choices.split(',')]
        return []

class ProfileData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(ProfileField, on_delete=models.CASCADE)
    value = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'field']

    def __str__(self):
        return f"{self.user.username} - {self.field.name}: {self.value}"

class UserStatus(models.Model):
    STATUS_CHOICES = [
        ('action', 'Action Required'),
        ('pending', 'Pending'),
        ('accept', 'Accepted'),
        ('reject', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='action')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"

    def get_status_icon(self):
        icons = {
            'action': '⚠️',
            'pending': '⏳',
            'accept': '✅',
            'reject': '❌',
        }
        return icons.get(self.status, '❓')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('president', 'President'),
        ('chairman', 'Chairman'),
        ('member', 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    birth_place = models.CharField(max_length=100)
    permanent_address = models.TextField()
    blood_group = models.CharField(max_length=10)
    post_code = models.CharField(max_length=20)
    post_office = models.CharField(max_length=100)
    upozilla = models.CharField(max_length=100)
    zila = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
