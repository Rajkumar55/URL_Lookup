from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import URLBlacklist


# Register your models here.
class URLBlacklistAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ['url']
    list_display = ['id', 'url', 'is_restricted', 'created_date', 'modified_date']
    list_filter = ['is_restricted']

admin.site.register(URLBlacklist, URLBlacklistAdmin)
