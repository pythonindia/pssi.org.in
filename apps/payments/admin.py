from django.contrib import admin
from .models import PaymentGateway, PaymentType, Payment

admin.site.register([PaymentGateway, PaymentType, Payment])
