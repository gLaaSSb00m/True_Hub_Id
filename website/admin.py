from django.contrib import admin
from .models import Article, ProfileField, ProfileData, Notification, Profile, UserStatus

# Register your models here.
admin.site.register(Article)
admin.site.register(ProfileField)
admin.site.register(ProfileData)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(UserStatus)
