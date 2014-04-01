from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext


def Auth(request):
	return render_to_response('cafe/auth.html', context_instance=RequestContext(request))

def Welcome(request):
	return render_to_response('cafe/welcome.html', context_instance=RequestContext(request))