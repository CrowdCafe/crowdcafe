from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from mobi.decorators import detect_mobile
@detect_mobile
def Home(request):
	if request.user.is_authenticated():
		if request.mobile:
			return redirect('cafe-home')
		return redirect('kitchen-home')
	else:
		return redirect('welcome')
@detect_mobile
def Welcome(request):
	if request.mobile:
		return redirect('cafe-welcome')
	return render_to_response('landing/welcome.html', context_instance=RequestContext(request))