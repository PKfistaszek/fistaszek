# -*- coding: utf-8 -*-
import factory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from myproject.models import UserFiles


class UserFactory(factory.Factory):
    class Meta:
        model = User


class UserFilesFactory(factory.Factory):
    # upload = SimpleUploadedFile("file.JSON", "file_content", content_type="aplication/JSON", name="upload/file.JSON")

    class Meta:
        model = UserFiles
