from django.contrib import admin

# Register your models here.

from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'check_in', 'check_out', 'total_price', 'user', 'organization', 'approved_by', 'status', 'pin_code', 'is_active', 'created_at')


admin.site.register(Reservation, ReservationAdmin)
