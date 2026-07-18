from django.contrib import admin
from .models import UserProfile, Track, LabelApplication, StudioInfo

# Register your models here so they appear in the Django admin panel
admin.site.register(UserProfile)
admin.site.register(Track)
admin.site.register(LabelApplication)
admin.site.register(StudioInfo)