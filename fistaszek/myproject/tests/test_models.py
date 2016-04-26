# -*- coding: utf-8 -*-
u"""
Testy modeli.
=============
"""

from mock import Mock, patch, sentinel
from morelia.decorators import tags
from smarttest.decorators import no_db_testcase

from django.core.files import File
from django.test import TestCase

from myproject.factories import UserFilesFactory


@no_db_testcase
@tags(['unit'])
class UserFilesTestCase(TestCase):
    u"UserFiles unittest class."

    def test_shoud_return_name_described_by_unicode(self):
        u""" Test for __unicode__ function."""
        file = Mock(File)
        file.name = 'upload/fake.JSON'
        user_file = UserFilesFactory.build(pk=1, upload=file)
        self.assertEqual('fake.JSON', user_file.__unicode__())
