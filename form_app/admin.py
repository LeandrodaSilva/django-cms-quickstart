from django.contrib import admin

from form_app.models import Form, FormSubmission


class FormSubmissionInline(admin.TabularInline):
    model = FormSubmission
    extra = 0
    can_delete = False
    readonly_fields = ("submitted_at", "data")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """Admin para configuração do formulário"""
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [FormSubmissionInline]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ['name', 'action']
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ("form", "submitted_at")
    list_filter = ("form", "submitted_at")
    search_fields = ("form__name",)
    readonly_fields = ("form", "submitted_at", "data")
