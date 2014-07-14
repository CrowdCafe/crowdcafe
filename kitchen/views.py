import logging
import re
import csv
import urllib2
import StringIO

from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from social_auth.models import UserSocialAuth
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage as s3_storage
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from models import App, Job, QualityControl, Unit, Judgement
from account.models import Account
from forms import AppForm, JobForm, QualityControlForm, UnitForm, JudgementForm


log = logging.getLogger(__name__)

# -------------------------------------------------------------
# Apps
# -------------------------------------------------------------
class AppCreateView(CreateView):
    model = App
    template_name = "kitchen/crispy.html"
    form_class = AppForm

    def get_initial(self):
        initial = {}
        initial['creator'] = self.request.user
        initial['account'] = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None))
        return initial

    def form_invalid(self, form):
        log.debug("form is not valid")
        return CreateView.form_invalid(self, form)

    def form_valid(self, form):
        log.debug("saved")
        app = form.save()
        app.save()

        return redirect(reverse('app-list', kwargs={'account_pk': app.account.id}))


class AppUpdateView(UpdateView):
    model = App
    template_name = "kitchen/crispy.html"
    form_class = AppForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(App, pk=self.kwargs.get('app_pk', None), creator=self.request.user)

    def form_valid(self, form):
        log.debug("updated")
        app = form.save()
        return redirect(reverse('app-list', kwargs={'account_pk': app.account.id}))


class AppListView(ListView):
    model = App
    template_name = "kitchen/app_list.html"

    def get_queryset(self):
        account = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None), users__in=[self.request.user.id])
        return App.objects.filter(account=account)

    def get_context_data(self, **kwargs):
        context = super(AppListView, self).get_context_data(**kwargs)
        context['account'] = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None))
        return context


# -------------------------------------------------------------
# Jobs
# -------------------------------------------------------------
class JobCreateView(CreateView):
    model = Job
    template_name = "kitchen/crispy.html"
    form_class = JobForm

    def get_initial(self):
        initial = {}
        initial['creator'] = self.request.user
        initial['app'] = get_object_or_404(App, pk=self.kwargs.get('app_pk', None), account__users__in=[self.request.user.id])
        return initial

    def form_invalid(self, form):
        log.debug("form is not valid")
        print form.errors
        return CreateView.form_invalid(self, form)

    def form_valid(self, form):
        log.debug("saved")
        job = form.save()
        job.save()

        return redirect(reverse('job-list', kwargs={'app_pk': job.app.id}))

class JobUpdateView(UpdateView):
    model = Job
    template_name = "kitchen/crispy.html"
    form_class = JobForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Job, pk=self.kwargs.get('job_pk', None), app__account__users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        job = form.save()
        return redirect(reverse('job-list', kwargs={'app_pk': job.app.id}))


class JobListView(ListView):
    model = Job
    template_name = "kitchen/job_list.html"

    def get_queryset(self):
        app = get_object_or_404(App, pk=self.kwargs.get('app_pk', None), account__users__in=[self.request.user.id])
        return Job.objects.filter(app=app)

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['app'] = get_object_or_404(App, pk=self.kwargs.get('app_pk', None))
        return context

# -------------------------------------------------------------
# QualityControl
# -------------------------------------------------------------
class QualityControlUpdateView(UpdateView):
    model = QualityControl
    template_name = "kitchen/crispy.html"
    form_class = QualityControlForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        job = get_object_or_404(Job, pk = self.kwargs.get('job_pk', None), app__account__users__in=[self.request.user.id])
        return job.qualitycontrol

    def form_valid(self, form):
        log.debug("updated")
        qualitycontrol = form.save()
        return redirect(reverse('job-list', kwargs={'app_pk': qualitycontrol.job.app.id}))
# -------------------------------------------------------------
# Units
# -------------------------------------------------------------
# Upload of units is in utility.views.AttachmentCreateView

class UnitListView(ListView):
    model = Job
    template_name = "kitchen/unit_list.html"

    def get_queryset(self):
        job = get_object_or_404(Job, pk=self.kwargs.get('job_pk', None), app__account__users__in=[self.request.user.id])
        return Unit.objects.filter(job=job)

    def get_context_data(self, **kwargs):
        context = super(UnitListView, self).get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs.get('job_pk', None))
        return context

class UnitUpdateView(UpdateView):
    model = Unit
    template_name = "kitchen/crispy.html"
    form_class = UnitForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Unit, pk=self.kwargs.get('unit_pk', None), job__app__account__users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        unit = form.save()
        return redirect(reverse('unit-list', kwargs={'job_pk': unit.job.id}))

# -------------------------------------------------------------
# Judgements
# -------------------------------------------------------------
# Creation of judgements is done via Cafe app

class JudgementListView(ListView):
    model = Judgement
    template_name = "kitchen/judgement_list.html"

    def get_queryset(self):
        unit = get_object_or_404(Unit, pk=self.kwargs.get('unit_pk', None), job__app__account__users__in=[self.request.user.id])
        return Judgement.objects.filter(unit=unit)

    def get_context_data(self, **kwargs):
        context = super(JudgementListView, self).get_context_data(**kwargs)
        context['unit'] = get_object_or_404(Unit, pk=self.kwargs.get('unit_pk', None))
        return context

class JudgementUpdateView(UpdateView):
    model = Judgement
    template_name = "kitchen/crispy.html"
    form_class = JudgementForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Judgement, pk=self.kwargs.get('judgement_pk', None), unit__job__app__account__users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        judgement = form.save()
        return redirect(reverse('unit-list', kwargs={'unit_pk': judgement.unit.id}))