from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
import uuid
from account.models import Account
from models import Vendor, Reward, Coupon
from forms import VendorForm, RewardForm, CouponForm
import logging

log = logging.getLogger(__name__)
# -------------------------------------------------------------
# Vendors
# -------------------------------------------------------------
class VendorCreateView(CreateView):
    model = Vendor
    template_name = "kitchen/crispy.html"
    form_class = VendorForm

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
        vendor = form.save()
        vendor.save()

        return redirect(reverse('vendor-list', kwargs={'account_pk': vendor.account.id}))

class VendorUpdateView(UpdateView):
    model = Vendor
    template_name = "kitchen/crispy.html"
    form_class = VendorForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Vendor, pk=self.kwargs.get('vendor_pk', None), account__users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        vendor = form.save()
        return redirect(reverse('vendor-list', kwargs={'account_pk': vendor.account.id}))

class VendorListView(ListView):
    model = Vendor
    template_name = "rewards/vendor_list.html"

    def get_queryset(self):
    	account = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None), users__in=[self.request.user.id])
        return Vendor.objects.filter(account = account)

    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        context['account'] = get_object_or_404(Account, pk=self.kwargs.get('account_pk', None))
        return context

# -------------------------------------------------------------
# Rewards
# -------------------------------------------------------------
class RewardCreateView(CreateView):
    model = Reward
    template_name = "kitchen/crispy.html"
    form_class = RewardForm

    def get_initial(self):
        initial = {}
        initial['creator'] = self.request.user
        initial['vendor'] = get_object_or_404(Vendor, pk=self.kwargs.get('vendor_pk', None), account__users__in=[self.request.user.id])
        return initial

    def form_invalid(self, form):
        log.debug("form is not valid")
        return CreateView.form_invalid(self, form)

    def form_valid(self, form):
        log.debug("saved")
        reward = form.save()
        reward.save()

        return redirect(reverse('reward-list', kwargs={'vendor_pk': reward.vendor.id}))

class RewardUpdateView(UpdateView):
    model = Reward
    template_name = "kitchen/crispy.html"
    form_class = RewardForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Reward, pk=self.kwargs.get('reward_pk', None), vendor__account__users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        reward = form.save()
        return redirect(reverse('reward-list', kwargs={'vendor_pk': reward.vendor.id}))

class RewardListView(ListView):
    model = Reward
    template_name = "rewards/reward_list.html"

    def get_queryset(self):
    	vendor = get_object_or_404(Vendor, pk=self.kwargs.get('vendor_pk', None), account__users__in=[self.request.user.id])
        return Reward.objects.filter(vendor = vendor)

    def get_context_data(self, **kwargs):
        context = super(RewardListView, self).get_context_data(**kwargs)
        context['vendor'] = get_object_or_404(Vendor, pk=self.kwargs.get('vendor_pk', None), account__users__in=[self.request.user.id])
        return context

# -------------------------------------------------------------
# Coupons
# -------------------------------------------------------------

class CouponListView(ListView):
    model = Coupon
    template_name = "rewards/coupon_list.html"

    def get_queryset(self):
    	reward = get_object_or_404(Reward, pk=self.kwargs.get('reward_pk', None), vendor__account__users__in=[self.request.user.id])
        return Coupon.objects.filter(reward = reward)

    def get_context_data(self, **kwargs):
        context = super(CouponListView, self).get_context_data(**kwargs)
        context['reward'] = get_object_or_404(Reward, pk=self.kwargs.get('reward_pk', None), vendor__account__users__in=[self.request.user.id])
        return context

class CouponUpdateView(UpdateView):
    model = Coupon
    template_name = "kitchen/crispy.html"
    form_class = CouponForm

    def form_invalid(self, form):
        log.debug("form is not valid")
        return UpdateView.form_invalid(self, form)

    def get_object(self):
        return get_object_or_404(Coupon, pk=self.kwargs.get('coupon_pk', None), reward__vendor__account__users__in=[self.request.user.id])

    def form_valid(self, form):
        log.debug("updated")
        coupon = form.save()
        return redirect(reverse('coupon-list', kwargs={'reward_pk': coupon.reward.id}))