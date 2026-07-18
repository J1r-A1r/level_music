from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Track, LabelApplication, StudioInfo

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'stage_name', 'avatar', 'bio', 'is_verified_artist', 'created_at']
        read_only_fields = ['is_verified_artist', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    """Serializer for reading user data (includes profile details)"""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class RegisterSerializer(serializers.ModelSerializer):
    """Custom serializer for registering new Listeners or Artists"""
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)
    stage_name = serializers.CharField(max_length=150, required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role', 'stage_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract custom fields before creating the user
        role = validated_data.pop('role', 'listener')
        stage_name = validated_data.pop('stage_name', '')
        
        # Create standard Django user securely
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # Automatically create linked UserProfile with the chosen role
        UserProfile.objects.create(
            user=user,
            role=role,
            stage_name=stage_name if role == 'artist' else None
        )
        return user

class TrackSerializer(serializers.ModelSerializer):
    """Serializer for Tracks, includes artist's stage name dynamically"""
    artist_name = serializers.CharField(source='artist.profile.stage_name', read_only=True)

    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['views_count', 'created_at', 'artist']

class LabelApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelApplication
        fields = '__all__'
        read_only_fields = ['is_reviewed', 'submitted_at']

class StudioInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioInfo
        fields = '__all__'