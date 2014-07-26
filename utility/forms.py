from django import forms
from datetime import date, timedelta
from account.models import Account

from kitchen.models import Job, Attachment
from django.conf import settings

from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout

import logging
from decimal import Decimal
from django.utils.datetime_safe import datetime
from django.forms.forms import Form
from django.forms.fields import FileField

log = logging.getLogger(__name__)

class AttachmentForm(ModelForm):
	job = forms.ModelChoiceField(queryset=Job.objects.all(), widget=forms.HiddenInput)
	
	class Meta:
		model = Attachment
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Upload'))
		self.helper.form_class = 'form-vertical'
		super(AttachmentForm, self).__init__(*args, **kwargs)