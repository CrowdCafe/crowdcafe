__author__ = 'stefano'
from rest_framework_nested.routers import  SimpleRouter, NestedSimpleRouter


class ApiRouter(SimpleRouter):

    def get_default_base_name(self, viewset):
        return "api-"+super(SimpleRouter, self).get_default_base_name(viewset)


class NestedApiRouter(NestedSimpleRouter):
    def get_default_base_name(self, viewset):
        return "api-"+super(NestedSimpleRouter, self).get_default_base_name(viewset)
