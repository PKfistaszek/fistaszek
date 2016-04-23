# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0002_userfiles_upload_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfiles',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
