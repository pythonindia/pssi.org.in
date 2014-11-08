from django.db import models
from django.conf import settings
from common.models import BaseModel
from django_pgjson.fields import JsonField

PAYMENT_STATUS_CHOICES = (
    ('p', 'Pending'),
    ('r', 'Received'),
    ('c', 'Cancelled'),
    ('f', 'Refunded')
)


class PaymentGateway(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField("API Key", max_length=100)
    auth_token = models.CharField("Auth Token", max_length=100)
    webhook_salt = models.CharField(
        "Salt for Webhook", max_length=100, blank=True, null=True
    )

    def __str__(self):
        return self.name


class PaymentType(BaseModel):
    """
    E.g. Membership, Donation
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Payment(BaseModel):
    gateway = models.ForeignKey("PaymentGateway")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    ptype = models.ForeignKey("PaymentType")
    payment_id = models.CharField(
        "Payment ID", max_length=50, blank=True, null=True
    )
    amount = models.FloatField(default=0.0)
    status = models.CharField(
        "Status", max_length=1, choices=PAYMENT_STATUS_CHOICES
    )
    status_pg = models.CharField(
        "Status from Payment Gateway", max_length=50
    )
    # store the whole json response
    raw_details = JsonField()

    def __str__(self):
        return self.user.get_full_name(), self.gateway, self.created_at
