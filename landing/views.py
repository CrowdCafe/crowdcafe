from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext


def Home(request):
	if request.user.is_authenticated():
		return redirect('kitchen-home')
	else:
		return redirect('welcome')
def Welcome(request):
    return render_to_response('landing/welcome.html', context_instance=RequestContext(request))
    
