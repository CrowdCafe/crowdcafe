'''
This file contains the permission rules for the api.

'''
from kitchen.models import App, Job, Unit, Judgement

__author__ = 'stefano'


import logging

from rest_framework.permissions import SAFE_METHODS


from rest_framework import permissions


log = logging.getLogger(__name__)


class IsOwner(permissions.BasePermission):
    '''
        check if user is owner of the object
    '''
    def has_permission(self, request, view, obj=None):
        # log.debug("check permission")
        #if it's a task instance check ownership of the task

        if obj is None:
             log.debug('none')
             return True
        # for app instance return true
        elif isinstance(obj,App):
            log.debug('app')
            return True
        # if it's a job
        elif isinstance(obj,Job):
            log.debug('job %s %s %s %s'%(obj.pk, obj.app,request.app,obj.app==request.app))
            return obj.app==request.app
        # if it's a unit
        elif isinstance(obj,Unit):
            log.debug('unit %s %s %s'%(obj.job.app,request.app,obj.job.app==request.app))
            return obj.job.app==request.app
        # if it's a judgement
        elif isinstance(obj,Judgement):
            log.debug('judgement %s %s %s'%(obj.unit.job.app,request.app,obj.unit.job.app==request.app))
            return obj.unit.job.app==request.app
        else:
            log.debug('is smt else')
            return False


class IsExecutor(permissions.BasePermission):
    '''
    check if user is worker of the object.
    '''
    def has_object_permission(self, request, view, obj):
        #if it's a task instance check ownership of the task
        if hasattr(obj, 'executor'):
            return obj.task.executor == request.user
        else:
            return False


# class IsFromApp(permissions.BasePermission):
#     def has_permission(self, request, view, obj=None):
#         if request.method in SAFE_METHODS:
#             return True
#         apptoken = request.app.token
#         if apptoken is None:
#             return False
#         try:
#             pass
#             #     enable this
#             #     App.objects.get(token=apptoken,owner=request.user)
#             return True
#         except Exception as e:
#             return False