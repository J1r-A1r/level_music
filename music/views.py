from rest_framework import generics, viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User

from .models import Track, LabelApplication, StudioInfo
from .serializers import (
    RegisterSerializer, 
    TrackSerializer, 
    LabelApplicationSerializer, 
    StudioInfoSerializer
)

class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration (Artists and Listeners)"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # Anyone can register
    serializer_class = RegisterSerializer


class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tracks to be viewed or edited.
    Provides GET (list), POST (create), GET (detail), PUT, DELETE out of the box.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    # Anyone can listen (read), but only logged-in users can upload
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Required to correctly process files (audio and images) from React frontend
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # Automatically assign the uploaded track to the user who sent the request
        serializer.save(artist=self.request.user)


class LabelApplicationCreateView(generics.CreateAPIView):
    """API endpoint for submitting a demo to the label"""
    queryset = LabelApplication.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = LabelApplicationSerializer


class StudioInfoListView(generics.ListAPIView):
    """API endpoint to fetch About Us / Studio info for the frontend"""
    queryset = StudioInfo.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = StudioInfoSerializer