from django.contrib import admin
from .models import Meeting, Ticket, Donor


class DonorAdmin(admin.ModelAdmin):
    list_display = (
        'campaign',
        'first_name',
        'last_name',
        'amount',
        'currency',
        'mail_sent'
    )


admin.site.register(Meeting)
admin.site.register(Ticket)
admin.site.register(Donor, DonorAdmin)
