# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class UserFiles(models.Model):
    u"UserFiles model."
    upload = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User)
    upload_date = models.DateTimeField(default=datetime.now(), blank=True)
    private = models.BooleanField(default=False)

    def __unicode__(self):
        name = self.upload.name.split('/')[1]
        return name
