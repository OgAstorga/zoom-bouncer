from django.contrib import admin
from .models import Meeting, Ticket, Donor


admin.site.register(Meeting)
admin.site.register(Ticket)
admin.site.register(Donor)
