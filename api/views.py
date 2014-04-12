from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, JSONPRenderer

from rest_framework_csv import renderers as r
from rest_framework.settings import api_settings

from kitchen.models import Task, TaskInstance, DataItem
from serializers import TaskSerializer,TaskInstanceSerializer, UserSerializer,AnswerDataCSVSerializer


import requests

@api_view(['GET'])
@login_required
def getUser(request):
	serializer = UserSerializer(request.user)
	return Response(serializer.data)

@api_view(['GET'])
def getTasks(request):
	tasks = Task.objects.filter(status = 'ST').all()
	serializer = TaskSerializer(tasks)
	return Response(serializer.data)

@api_view(['GET'])
def getInstance(request, task_id):
	task = get_object_or_404(Task, pk = task_id)
	taskinstance = TaskInstance.objects.filter(task = task).all()[0]
	serializer = TaskInstanceSerializer(taskinstance)
	return Response(serializer.data)

@api_view(['GET'])
@login_required
def getAnswers(request, task_id):
	taskinstances = TaskInstance.objects.filter(task__id = task_id,task__owner = request.user).all()
	serializer = TaskInstanceSerializer(taskinstances)
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
def getCSV(request, task_id):
	
	answeritems = []
	
	taskinstances = TaskInstance.objects.filter(task__id = task_id,task__owner = request.user).all()
	for taskinstance in taskinstances:
		for answer in taskinstance.answers:
			for answeritem in answer.answeritems:
				answeritems.append(answeritem)

	serializer = AnswerDataCSVSerializer(answeritems)
	return Response(serializer.data)