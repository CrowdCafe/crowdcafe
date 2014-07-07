from django import forms
from models import Vendor, Reward, Coupon
from account.models import Account

from django.conf import settings

from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout

import logging
from decimal import Decimal
from django.utils.datetime_safe import datetime
from django.forms.forms import Form

log = logging.getLogger(__name__)

class VendorForm(ModelForm):
	creator = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput)

	class Meta:
		model = Vendor
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		super(VendorForm, self).__init__(*args, **kwargs)

class RewardForm(ModelForm):
	vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput)
	creator = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	
	class Meta:
		model = Reward

	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		super(RewardForm, self).__init__(*args, **kwargs)

class CouponForm(ModelForm):

	class Meta:
		model = Coupon
		exclude = ('account', 'reward')

	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		super(CouponForm, self).__init__(*args, **kwargs)