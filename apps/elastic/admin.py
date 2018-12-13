from django.contrib import admin

from .models import QueryTemplate

# Register your models here.




class QueryTemplateAdmin (admin.ModelAdmin):
    list_display = ('user','name','title','template')
    #ordering = ('-datetime','user')
    list_filter = (
        ('user'),
    )


admin.site.register(QueryTemplate, QueryTemplateAdmin)
