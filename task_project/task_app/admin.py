from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin

class TastAdmin(ImportExportModelAdmin):
    list_display = ('title', 'description', 'created_at', 'due_date', 'is_completed')


admin.site.register(models.Task, TastAdmin)