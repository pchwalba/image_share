from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from . import api_views

router = DefaultRouter()

urlpatterns = [path('images/', api_views.UserImages.as_view(), name='images'),
               path('upload/', api_views.ImageUpload.as_view(), name='upload'),
               path("expiring-links/", api_views.ExpiringLinkListCreateView.as_view(), name='expiring-link-create-list'),
               path("expiring-links/<str:signed_link>/", api_views.ExpiringLinkDetailView.as_view(),
                    name='expiring-link-detail'),
               ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
