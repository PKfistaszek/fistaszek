from django.contrib import admin
from myproject.models import UserFiles
# Register your models here.


class UserFilesAdmin(admin.ModelAdmin):
    fields = ('upload', 'user', 'private', 'upload_date')


admin.site.register(UserFiles, UserFilesAdmin)
