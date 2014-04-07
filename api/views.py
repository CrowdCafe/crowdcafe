from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, JSONPRenderer

from kitchen.models import Task, TaskInstance, DataItem
from serializers import TaskSerializer,TaskInstanceSerializer, UserSerializer
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