from kitchen.models import Task, TaskInstance, DataItem

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


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    class Meta:
        model = Task
        fields = ('id','owner', 'title','description','category','template','status','date_created','date_deadline')

class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = ('id','value')

class TaskInstanceSerializer(serializers.ModelSerializer):
    dataitems = DataItemSerializer(many=True)
    class Meta:
        model = TaskInstance
        fields = ('id','dataitems')