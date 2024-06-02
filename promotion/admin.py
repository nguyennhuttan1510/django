from django.contrib import admin

# Register your models here.
from django.contrib import admin

from promotion.models import Promotion, PromotionItem


# Register your models here.

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date', 'created_at']


admin.site.register(Promotion, PromotionAdmin)


class PromotionItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'code', 'discount', 'discount_type', 'amount', 'start_date', 'end_date',
                    'created_at']


admin.site.register(PromotionItem, PromotionItemAdmin)
