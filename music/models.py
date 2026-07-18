from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    """Extends standard Django User to support Listener and Artist roles"""
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('artist', 'Artist'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='listener')
    stage_name = models.CharField(max_length=150, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_verified_artist = models.BooleanField(default=False, verbose_name="Verified Label Artist")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Track(models.Model):
    """Tracks uploaded by Artists or Label management"""
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='covers/')
    audio_file = models.FileField(
        upload_to='tracks/', 
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'flac'])]
    )
    
    # AI Analysis Fields (BPM, Key, and auto-generated tags)
    bpm = models.IntegerField(blank=True, null=True)
    music_key = models.CharField(max_length=20, blank=True, null=True)
    ai_tags = models.JSONField(default=list, blank=True)

    # Premiere Feature (Real-time countdown target)
    is_premiere = models.BooleanField(default=False)
    premiere_date = models.DateTimeField(blank=True, null=True)
    
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - Track ID: {self.id}"


class LabelApplication(models.Model):
    """Form data when an artist wants to join Level Music label"""
    full_name = models.CharField(max_length=255)
    stage_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    demo_link = models.URLField(help_text="Link to SoundCloud, Google Drive, DropBox, etc.")
    social_media = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(help_text="Tell us about yourself and your musical goals")
    is_reviewed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Application from {self.stage_name} ({self.full_name})"


class StudioInfo(models.Model):
    """Information about Level Music Studio, School, and About Us section"""
    section_title = models.CharField(max_length=200)
    description = models.TextField()
    showcase_image = models.ImageField(upload_to='studio/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.section_title