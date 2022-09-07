from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AuthByTokenMixin(object):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class AuthByNoneMixin(object):
    authentication_classes = []
    permission_classes = []