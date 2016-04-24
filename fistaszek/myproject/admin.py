from django.contrib import admin
from myproject.models import UserFiles


class UserFilesAdmin(admin.ModelAdmin):
    fields = ('upload', 'user', 'private', 'upload_date', )
    list_display = ('pk', 'upload', 'user', 'private', )
    list_filter = ('user', 'private', )
    raw_id_fields = ('user', )
    search_fields = ['user__username', ]

admin.site.register(UserFiles, UserFilesAdmin)
