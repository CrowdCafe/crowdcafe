# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login

from events.utils import logEvent

def Logout(request):
	logEvent(request, 'logout')
	logout(request)
	return redirect('welcome')