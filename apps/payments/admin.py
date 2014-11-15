from django.contrib import admin
from .models import PaymentGateway, PaymentType, Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'ptype', 'created_at', 'gateway', 'amount')
    search_fields = ('payment_id',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register([PaymentGateway, PaymentType])
