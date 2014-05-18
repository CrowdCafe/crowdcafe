from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.template import RequestContext

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, JSONPRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_csv import renderers as r
from rest_framework.settings import api_settings

from kitchen.models import Job, Task, DataItem
from serializers import JobSerializer,TaskSerializer, UserSerializer,AnswerDataCSVSerializer

from rest_framework.authtoken.models import Token

from kitchen.utils import saveDataItems


import requests

@login_required
def home(request):
	if Token.objects.filter(user=request.user).count() == 0:
		token = Token.objects.create(user=request.user)
	else:
		token = Token.objects.filter(user=request.user).all()[0]

	return render_to_response('api/home.html',{'token':token}, context_instance=RequestContext(request))

@api_view(['POST'])
def uploadItems(request, job_id):

	job = get_object_or_404(Job, pk = job_id, owner = request.user)

	print job.id
	print request.POST
	print request.user.id

	if request.POST:
		print 'dataset exists'
		saveDataItems(job,[request.POST])
		
	return Response()

@api_view(['GET'])
def getUser(request):
	serializer = UserSerializer(request.user)
	return Response(serializer.data)

@api_view(['GET'])
def getJobs(request):
	tasks = Job.objects.filter(status = 'ST').all()
	serializer = JobSerializer(tasks)
	return Response(serializer.data)

@api_view(['GET'])
def getTask(request, job_id):
	job = get_object_or_404(Job, pk = job_id)
	task = Task.objects.filter(task = task).all()[0]
	serializer = TaskSerializer(task)
	return Response(serializer.data)

@api_view(['GET'])
@login_required
def getAnswers(request, job_id):
	tasks = Task.objects.filter(job__id = job_id,job__owner = request.user).all()
	serializer = TaskSerializer(taskinstances)
	return Response(serializer.data)

@login_required
def readUrl(request):
	output = 'nothing'
	if 'url' in request.GET:
		url = 'http://en.m.wikipedia.org/wiki/'+request.GET['url']
		f = requests.get(url)
		output = f.text
	return HttpResponse(output)


@api_view(['GET'])
@login_required
def getCSV(request, job_id):
	answeritems = []
	tasks = Task.objects.filter(job__id = task_id,job__owner = request.user)
	if 'status' in request.GET:
		tasks.filter(status = request.GET['status'])
	tasks = tasks.all()
	for task in tasks:
		for answer in task.answers:
			for answeritem in answer.answeritems:
				answeritems.append(answeritem)

	serializer = AnswerDataCSVSerializer(answeritems)
	return Response(serializer.data)