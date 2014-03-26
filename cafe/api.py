from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, JSONPRenderer


from kitchen.models import Task, TaskInstance, DataItem
from serializers import TaskSerializer,TaskInstanceSerializer


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
	