from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from kitchen.models import Task, TaskInstance

def Welcome(request):
	return render_to_response('cafe/welcome.html', context_instance=RequestContext(request))

def Home(request):
	if request.user.is_authenticated():
		return render_to_response('cafe/home.html', context_instance=RequestContext(request))
	else:
		return redirect('cafe-welcome')

def TaskList(request):
	tasks = Task.objects.filter(status = 'ST').all()
	return render_to_response('cafe/home/pages/tasklist.html', {'tasks':tasks}, context_instance=RequestContext(request))

def TaskInstanceAssign(request, task_id):
	task = get_object_or_404(Task, pk = task_id, status = 'ST')

	instance = TaskInstance.objects.filter(task = task).all()[0]
	if instance:
		return redirect(reverse('cafe-taskinstance-execute', kwargs={'instance_id': instance.id}))
	else:
		return redirect('cafe-task-list')

def TaskInstanceExecute(request, instance_id):
	taskinstance = get_object_or_404(TaskInstance,pk = instance_id)
	return render_to_response('cafe/home/pages/task.html', {'taskinstance':taskinstance}, context_instance=RequestContext(request))