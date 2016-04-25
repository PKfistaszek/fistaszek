# -*- coding: utf-8 -*-
"""
Forms
==========
"""

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from myproject.models import UserFiles
from myproject.fields import RestrictedFileField


class UserForm(ModelForm):
    u"""
        UserForm responsible for logging.

        :param email: User email
        :type email: EmailField
        :param password: User password
        :type password: CharField.
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password']


class UploadFileForm(forms.Form):
    u"""
        UserForm responsible for uploading files.

        :param file: Uploaded file
        :type file: RestrictedFileField
        :param private: True if file is private
        :type private: bool.
    """
    file = RestrictedFileField(
        content_types=['application/json'],
        label='Select a file',
        help_text='max. 1 megabytes'
    )
    private = forms.BooleanField(initial=False, required=False, label='Private')
