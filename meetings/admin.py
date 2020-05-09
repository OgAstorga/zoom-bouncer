from django.contrib import admin
from .models import Meeting, Ticket, Donor


class DonorAdmin(admin.ModelAdmin):
    list_display = (
        'campaign',
        'first_name',
        'last_name',
        'amount',
        'currency',
        'donation_date',
        'mail_sent'
    )


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'usages',
        'max_usages',
    )


admin.site.register(Meeting)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Donor, DonorAdmin)
