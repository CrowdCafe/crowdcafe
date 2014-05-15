from kitchen.models import Job, Task, DataItem, Answer, AnswerItem

from django.contrib.auth.models import User
from account.models import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
	#url = serializers.CharField(source='url', read_only=True)
	short_name = serializers.CharField(source='short_name', read_only=True)
	full_name = serializers.CharField(source='full_name', read_only=True)
	class Meta:
		model = Profile
		fields = ('short_name','full_name')

class UserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer(many=False)
	class Meta:
		model = User
		fields = ('id','first_name','last_name','email','profile')


class JobSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    class Meta:
        model = Job
        fields = ('id','owner', 'title','description','category','template','status','date_created','date_deadline')

class AnswerSerializer(serializers.ModelSerializer):
    executor = UserSerializer(many=False)
    class Meta:
        model = Answer
        fields = ('id','executor','date_created','status')

class AnswerItemSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=False)
    class Meta:
        model = AnswerItem
        fields = ('id','value','answer')

class DataItemSerializer(serializers.ModelSerializer):
    answeritems = AnswerItemSerializer(many = True)
    class Meta:
        model = DataItem
        fields = ('id','answeritems')



class TaskSerializer(serializers.ModelSerializer):
    dataitems = DataItemSerializer(many=True)
    class Meta:
        model = Task
        fields = ('id','dataitems')

class AnswerDataCSVSerializer(serializers.ModelSerializer):
    date_created = serializers.CharField(source='date_created', read_only=True)
    question = serializers.CharField(source='question', read_only=True)
    value = serializers.CharField(source='value', read_only=True)
    worker_id = serializers.IntegerField(source='worker_id', read_only=True)
    #dataitem_id = serializers.IntegerField(source='dataitem_id', read_only=True)
    task_id = serializers.IntegerField(source='task_id', read_only=True)
    task_status = serializers.CharField(source='task_status', read_only=True)
    class Meta:
        model = AnswerItem
        fields = ('question','worker_id','id','value','date_created','task_id','task_status')