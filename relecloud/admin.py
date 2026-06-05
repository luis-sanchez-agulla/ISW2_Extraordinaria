from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Cruise)
admin.site.register(models.Destination)
admin.site.register(models.InfoRequest)


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('title', 'comment', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información de la reseña', {
            'fields': ('user', 'rating', 'title', 'comment')
        }),
        ('Destino o Crucero', {
            'fields': ('destination', 'cruise')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
