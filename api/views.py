import json
import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, action
from rest_framework.generics import get_object_or_404,UpdateAPIView
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from rest_framework import routers, viewsets, status, routers
from rest_framework import exceptions 

from api import routers
from api.routers import ApiRouter, NestedApiRouter

from api.serializers import JobSerializer, AppSerializer, UnitSerializer, JudgementSerializer
from kitchen.models import Job, App, Unit, Judgement
from serializers import UserSerializer

from rest_framework_nested import routers
from utility.utils import notifySuperUser

log = logging.getLogger(__name__)

# class AccountView(viewsets.ModelViewSet):
#     """
#     CRUD of Account
#     """
#     model = Account
#     serializer_class = AccountSerializer
#
#     def pre_save(self, obj):
#         # init values
#         user = self.request.user
#         obj.creator = user
#
#     # used to filter out based on the url
#     def get_queryset(self):
#         return Account.objects.filter(creator=self.request.user)
#
# class UserView(viewsets.ModelViewSet):
#     model = User
#     serializer_class = UserSerializer
#
#     def list(self, request, *args, **kwargs):
#         log.debug("it's the list")
#         log.debug("pk %s", self.kwargs['task_pk'])
#         ''' this checks if the user owns the task, if so then the instances are displayed,
#         if it's not his task then there's an exeception.
#          it's a dirty way to do auth'''
#
#         return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
#
#     def get_queryset(self):
#         return Account.objects.get(pk=self.kwargs['account_pk']).users

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def me(request):
    user_serilized = UserSerializer(request.user)
    return Response(user_serilized.data)


class AppViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    for the app, only readonly
    '''
    model = App
    serializer_class = AppSerializer

    def get_queryset(self):
        #  the job of the user with the requested app
        return App.objects.filter(account__in=self.request.user.account_set.all())


class JobsViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    model = Job
    paginate_by = 10



    # this should not be needed, it's handled by the permission
    def get_queryset(self):
        #  the job of the user with the requested app
        # ASK: filtering only by app?
        return Job.objects.filter(app=self.request.app)

    def create(self, request):
        # disable this function
        raise exceptions.MethodNotAllowed('CREATE')

    def destroy(self, request, pk=None):
        # disable this function
        raise exceptions.MethodNotAllowed('DESTROY')

    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('UPDATE')

    def partial_update(self, request, pk=None):
        raise exceptions.MethodNotAllowed('PARTIAL UPDATE')

class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    model = Unit
    paginate_by = 10

    def get_object(self):
        try:
            print 'received uni object'
            print self.kwargs['pk']
            log.debug(self.kwargs)
            
            unit = Unit.objects.filter(pk=self.kwargs['pk'], job__app = self.request.app).get()
        except:
            raise exceptions.PermissionDenied()
        return unit
    def get_queryset(self):
        # we don't need any other control beacuse this is nested
        # so permission checks if app owns the job
        list = Unit.objects.filter(job=self.kwargs['job_pk'])
        return list

    def list(self, request, *args, **kwargs):
        try:
            Job.objects.get(pk=self.kwargs['job_pk'], app=request.app)
        except:
            raise exceptions.PermissionDenied()
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def create(self,request,job_pk):
        job = get_object_or_404(Job, pk=job_pk, app=request.app)
        input = request.DATA
        # it expects an array
        if isinstance(input,list):
            for d in input:
                Unit.objects.create(job=job, input_data=json.dumps(d))
        else:
            new_unit = Unit.objects.create(job=job, input_data=json.dumps(input))
            return new_unit
        # this notifies SU once a day
        notifySuperUser(job_pk)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        # disable this function
        raise exceptions.MethodNotAllowed('DESTROY')

    #def update(self, request, *args, **kwargs):
    #    raise exceptions.MethodNotAllowed('UPDATE')



    #def partial_update(self, request, pk=None):
    #    raise exceptions.MethodNotAllowed('PARTIAL UPDATE')


class JudgementViewSet(viewsets.ModelViewSet):
    serializer_class = JudgementSerializer
    model = Judgement
    paginate_by = 10

    def get_queryset(self):
        # we don't need any other control beacuse this is nested
        # so permission checks if app owns the job
        list = Judgement.objects.filter(unit=self.kwargs['unit_pk'])
        return list

    def list(self, request, *args, **kwargs):
        try:
            Unit.objects.get(pk=self.kwargs['unit_pk'], job__app=request.app)
        except:
            raise exceptions.PermissionDenied()
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def create(self,request,unit_pk):
        # disable this function
        raise exceptions.MethodNotAllowed('CREATE')

    def destroy(self, request, pk=None):
        # disable this function
        raise exceptions.MethodNotAllowed('DESTROY')

router = ApiRouter()

router.register(r'app', AppViewSet)
router.register(r'job', JobsViewSet)
router.register(r'unit', UnitViewSet)

job_router = NestedApiRouter(router, r'job', lookup='job')
job_router.register(r'unit', UnitViewSet)

unit_router = NestedApiRouter(router, r'unit', lookup='unit')
unit_router.register(r'judgement', JudgementViewSet)
