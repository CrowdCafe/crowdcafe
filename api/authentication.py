from __future__ import unicode_literals
import logging

__author__ = 'stefano'

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.authtoken.models import Token
from kitchen.models import App

log = logging.getLogger(__name__)
class TokenAppAuthentication(BaseAuthentication):
    """
        App token authentication, modified from TokenBase Authentication

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a|812cf2548f624b93d18e57820a0153accb03da2b

        it's apptoken|usertoken

        user must have authorized the app to act on his behalf.
    """

    model = App
    """
        Change this with your model, has to have the field 'owner'
        or change the rest of the code accordingly
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        # here we pass the request, this is needed to add the app.
        # No better solution found so far
        return self.authenticate_credentials(auth[1], request)

    def authenticate_credentials(self, key,request):
        '''
            the actual function that handles authentication
        '''
        # if only user
        if "|" in key:
            usertoken,apptoken = key.split("|")
        else:
            raise exceptions.AuthenticationFailed('Token is of the wrong format')

        try:
            # get the token via key
            token = Token.objects.get(key=usertoken)
            # get the app
            app = self.model.objects.get(token=apptoken)
            log.debug("%s %s %s"%(token.user.username,app.pk,app.title))

            # check if user is in the account of the app
            if not token.user in app.account.users.all():
                raise exceptions.AuthenticationFailed("You don't have the right to use this application")
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token for app')
        # not sure this is correct
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token for user')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if app:
            request.app=app
        return (token.user, token)

    def authenticate_header(self, request):
        return 'Token'