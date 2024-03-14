from django.contrib import admin

# Register your models here.

from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'check_in', 'check_out', 'balance_amount', 'guest', 'organization', 'approved_by', 'status', 'pin_code', 'is_active', 'evaluation')


admin.site.register(Reservation, ReservationAdmin)
