from rest_framework import permissions


class PublicEndpoint(permissions.BasePermission):
    """
    This permission make rest api free access, without authorization
    """
    def has_permission(self,request,view):
        return True
