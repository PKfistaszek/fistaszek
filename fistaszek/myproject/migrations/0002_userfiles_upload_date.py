# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfiles',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 23, 10, 30, 13, 138172, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
