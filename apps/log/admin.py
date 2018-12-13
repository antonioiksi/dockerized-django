from django.contrib import admin

from . import models

# Register your models here.


class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip', 'datetime', 'duration', 'query', 'event', 'method')
    ordering = ('-datetime', 'user')
    list_filter = (
        ('ip'), ('user'), ('event'),
    )


admin.site.register(models.Log, LogAdmin)
