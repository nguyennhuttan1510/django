from django.contrib import admin

from evaluation.models import Evaluation


# Register your models here.
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description_satisfied', 'description_unsatisfied', 'service', 'points', 'category', 'is_active',
        'created_at')

    def get_queryset(self, request):
        # Retrieve the current user
        current_user = request.user

        if current_user.is_staff or current_user.is_superuser:
            queryset = super().get_queryset(request)
            return queryset

        # Filter the queryset based on the owner field
        queryset = super().get_queryset(request).filter(user=current_user.pk)

        return queryset


admin.site.register(Evaluation, EvaluationAdmin)
