# -*- coding: utf-8 -*-
"""
Celery tasks
======
"""
from __future__ import absolute_import

from celery.decorators import task
from celery.utils.log import get_task_logger

from myproject.emails import send_upload_email


logger = get_task_logger(__name__)


@task(name="send_feedback_email_task")
def send_upload_email_task(email, message):
    u"Sends an email when file is uploaded successfully."
    logger.info("Sent upload email")
    return send_upload_email(email, message)
