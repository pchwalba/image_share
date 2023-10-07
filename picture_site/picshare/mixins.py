import time
import uuid
from django.core import signing
from django.urls import reverse
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from .models import ExpiringLink


class ExpiringLinkMixin:
    def generate_expiring_link(self, image, expires_in):
        user_tier = image.user.tier
        if not user_tier.expiring_link:
            raise PermissionDenied("Upgrade to Enterprise Tier to use this function")

        pk = uuid.uuid4()
        signed_link = signing.dumps(str(pk))

        full_url = self.request.build_absolute_uri(reverse('expiring-link-detail', kwargs={'signed_link': signed_link}))

        current_timestamp = int(time.time())
        expire_time = current_timestamp + expires_in

        ExpiringLink.objects.create(id=pk, link=full_url, image=image, expires_in=expire_time)

        return full_url

    @staticmethod
    def decode_signed_value(value: str) -> ExpiringLink.id:
        try:
            return signing.loads(value)
        except signing.BadSignature:
            raise NotFound("Invalid signed link")