# -*- coding: utf-8 -*-
"""
Factories
======
"""

import factory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from myproject.models import UserFiles


class UserFactory(factory.Factory):
    u"Factory class for User."
    class Meta:
        model = User


class UserFilesFactory(factory.Factory):
    u"Factory class for UserFilesFactory."

    class Meta:
        model = UserFiles
