# -*- coding: utf-8 -*-
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import (
    FormView,
    RedirectView,
    ListView,
)
from django import forms
from django.http import HttpResponseRedirect

from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned
)
from django.forms import ValidationError

from myproject.forms import UserForm, UploadFileForm
from myproject.models import UserFiles


class IndexView(FormView):
    u"Webstie index."

    template_name = 'index.html'
    form_class = UserForm

    def form_valid(self, form):
        user_email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user_object = User.objects.get(email=user_email)
        user = authenticate(username=user_object.username, password=password)
        login(self.request, user)
        return super(IndexView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated():
        #     return redirect('upload')
        return FormView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def get_success_url(self):
        return redirect('upload')


class LogoutView(RedirectView):
    u"View provides user logout."

    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UploadFileView(FormView):
    u"Logged user view with upload file form."

    template_name = 'upload.html'
    form_class = UploadFileForm

    def form_valid(self, form):
        user_file = UserFiles(
            upload=self.get_form_kwargs().get('files')['file'],
            user=self.request.user
        )
        user_file.save()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect('index')
        return FormView.get(self, request, *args, **kwargs)

    def get_success_url(self):
        return self.request.get_full_path()


class UploadFileList(ListView):
    u"View provides list view uploaded files"

    queryset = UserFiles.objects.order_by('-upload_date')
    model = UserFiles
    template_name = 'list.html'
