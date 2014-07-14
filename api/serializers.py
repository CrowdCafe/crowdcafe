# TODO - needs to be rewritten
from django.contrib.auth.models import User
from rest_framework import serializers

from kitchen.models import Job, Unit
from account.models import Profile, Account


class ProfileSerializer(serializers.ModelSerializer):
    shortname = serializers.CharField(source='shortname', read_only=True)
    fullname = serializers.CharField(source='fullname', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'shortname', 'fullname')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'profile')


class AccountSerializer(serializers.ModelSerializer):
    #creator = UserSerializer(many = False)
    #users = UserSerializer(many = True)

    class Meta:
        model = Account
        fields = ('id', 'title')


class JobSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    app = serializers.RelatedField(source='app.title', read_only=True)
    creator = serializers.RelatedField(source='creator.username', read_only=True)

    class Meta:
        model = Job
        read_only_fields = ('deleted', 'status', 'userinterface_html')


class AppSerializer(serializers.ModelSerializer):
    account = serializers.RelatedField(source='account.title', read_only=True)
    creator = serializers.RelatedField(source='creator.username', read_only=True)

    class Meta:
        model = Account
        fields = ('title', 'account', 'creator', 'title')

class UnitSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    class Meta:
        model = Unit
        fields=('input_data','status','pk')
        read_only_fields = ('status',)