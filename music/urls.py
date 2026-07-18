from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, 
    TrackViewSet, 
    LabelApplicationCreateView, 
    StudioInfoListView
)

# Using DRF router for ViewSets (automatically generates GET, POST, PUT, DELETE URLs)
router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    
    # Custom endpoints
    path('label-apply/', LabelApplicationCreateView.as_view(), name='label-apply'),
    path('studio-info/', StudioInfoListView.as_view(), name='studio-info'),
    
    # Include all auto-generated URLs from the router
    path('', include(router.urls)),
]