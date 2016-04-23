# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned
)
from django.forms import ValidationError
from django import forms
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from myproject.models import UserFiles
from myproject.fields import RestrictedFileField


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    '''
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        user_email = cleaned_data['email']
        password = cleaned_data['password']
        subject = cleaned_data.get("subject")
        user_object = User.objects.get(email=user_email)
        user = authenticate(username=user_object.username, password=password)

        print user
        if user is None:
            self.add_error('password', 'Invalid Password')'''


class UploadFileForm(forms.Form):
    file = RestrictedFileField(
        content_types=['application/pdf', 'application/json'],
        label='Select a file',
        help_text='max. 1 megabytes'
    )
'''
    def clean_file(self):
        CONTENT_TYPES = ['JSON']
        MAX_UPLOAD_FILE_SIZE = "1000000"
        content = self.cleaned_data['file']
        content_type = content.content_type.split('/')[0]
        if content_type in CONTENT_TYPES:
            if content._size > MAX_UPLOAD_PHOTO_SIZE:
                msg = 'Keep your file size under %s. actual size %s'\
                        % (filesizeformat(MAX_UPLOAD_FILE_SIZE), filesizeformat(content._size))
                raise forms.ValidationError(msg)

            if not content.name.endswith('.JSON'):
                msg = 'Your file is not JSON'
                raise forms.ValidationError(msg)
        else:
            raise forms.ValidationError('File not supported')
        return content'''
'''
class EmailAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.data['username']
        if '@' in username:
            try:
                username = User.objects.get(email=username).username
            except ObjectDoesNotExist:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.username_field.verbose_name},
                )
            except MultipleObjectsReturned:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return username
'''
