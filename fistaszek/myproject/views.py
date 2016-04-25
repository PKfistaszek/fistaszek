# -*- coding: utf-8 -*-
"""
Views
======
"""

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    FormView,
    RedirectView,
    ListView,
)

from myproject.forms import (
    UserForm,
    UploadFileForm
)
from myproject.models import UserFiles
from myproject.tasks import send_upload_email_task


class IndexView(FormView):
    u"""
        View responsible for user login.

        :param template_name: path to template
        :type template_name: string or unicode
        :param form_class: Logging form.`
        :type form_class: UserForm
        :param success_url: Return url after successful validation.
        :type success_url: specific django type ::module <django.utils.functional.__proxy__
    """

    template_name = 'index.html'
    form_class = UserForm
    success_url = reverse_lazy('upload')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('upload')
        return FormView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        user_email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user_object = User.objects.get(email=user_email)
        user = authenticate(username=user_object.username, password=password)
        login(self.request, user)
        return super(IndexView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class LogoutView(RedirectView):
    u"""
        View provides user logout..

        :param permanent: If true redirect is permanent.`
        :type permanent: bool
        :param url: Return url after successful logout.
        :type url: specific django type ::module <django.utils.functional.__proxy__
    """

    permanent = False
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UploadFileView(FormView):
    u"""
        Logged user view with upload file form.

        :param template_name: path to template`
        :type template_name: string or unicode
        :param form_class: Logging form.`
        :type form_class: UploadFileForm
    """

    template_name = 'upload.html'
    form_class = UploadFileForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return FormView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        user_file = UserFiles(
            upload=self.get_form_kwargs().get('files')['file'],
            user=self.request.user,
            private=form.cleaned_data['private']
        )
        user_file.save()
        message = self._send_create_email_message(user_file)

        send_upload_email_task(self.request.user.email, message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.get_full_path()

    def _send_create_email_message(self, user_file):
        u"Prepares content of mail and send it to send_upload_email_task."
        if user_file.private:
            private = 'Private'
        else:
            private = 'Public'
        message = "%s file %s uploaded." % (private, user_file)
        return message


class UploadFileList(ListView):
    u"""
        View provides list view public uploaded files.

        :param template_name: path to template
        :type template_name: string or unicode
        :param queryset: Returned queryset objects.
        :type queryset: QuerySet
    """

    queryset = UserFiles.objects.filter(private=False).order_by('-upload_date')
    model = UserFiles
    template_name = 'list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin_list')
        return ListView.dispatch(self, request, *args, **kwargs)


class AdminUploadFileList(ListView):
    u"""
        View provides list view all uploaded files for admin.

        :param template_name: path to template
        :type template_name: string or unicode
        :param queryset: Returned queryset objects.
        :type queryset: QuerySet.
    """

    queryset = UserFiles.objects.order_by('private')
    template_name = 'admin_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return ListView.dispatch(self, request, *args, **kwargs)
