from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import Task

@login_required
def Home(request):

	tasks = Task.objects.filter(owner = request.user).order_by('-date_created').all()
	return render_to_response('kitchen/home.html', {'tasks':tasks}, context_instance=RequestContext(request))

@login_required
def TaskNew(request):
	return render_to_response('kitchen/task.html', context_instance=RequestContext(request))

@login_required
def TaskSave(request):

	print request.FILES
	new_task = Task(owner = request.user, title = request.POST['task_title'],template = request.POST['task_uitemplate'],category = request.POST['task_category'])
	new_task.save()

	if request.FILES:
		new_task.dataset_file.save(str(new_task.id)+request.FILES['file'].name, request.FILES['file'])
		new_task.save()   
	return redirect('kitchen-home')