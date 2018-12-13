import datetime
import json
import logging
import socket
import time

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import Log

logger = logging.getLogger(__name__)

def get_user_jwt(request):
    """
    Replacement for django session auth get_user & auth.get_user
     JSON Web Token authentication. Inspects the token for the user_id,
     attempts to get that user from the DB & assigns the user on the
     request object. Otherwise it defaults to AnonymousUser.

    This will work with existing decorators like LoginRequired  ;)

    Returns: instance of user object or AnonymousUser object
    """
    user = None
    try:
        user_jwt = JWTTokenUserAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            token_user = user_jwt[0]
            user_id = token_user.pk
            user = User.objects.get(id=user_id)
    except:
        pass
    return user


def process_response(request, response):
    if response.get('content-type') == 'application/json':
        if getattr(response, 'streaming', False):
            response_body = '<<<Streaming>>>'
        else:
            response_body = response.content
    else:
        response_body = '<<<Not JSON>>>'

    log_data = {
        'user': request.user.pk,

        'remote_address': request.META['REMOTE_ADDR'],
        'server_hostname': socket.gethostname(),

        'request_method': request.method,
        'request_path': request.get_full_path(),
        # 'request_body': request.body,

        'response_status': response.status_code,
        'response_body': response_body,

        'run_time': time.time() - request.start_time,
    }

    logger.debug(log_data)
    return response


class RequestLogMiddleware(object):

    def process_request(self, request):
        user = get_user_jwt(request)
        request.user = user

        request.start_time = time.time()

        if request.method == 'POST':
            try:
                query = json.loads(request.body.decode("utf-8"))
            except Exception as err:
                logger.error("Error in posting json %s" % err)
                query = None
        else:
            query = None

        log = Log(user=user,
                  ip=request.META['REMOTE_ADDR'],
                  datetime=datetime.datetime.now(),
                  query=query,
                  method=request.method,
                  event=request.path_info)
        log.save()
        request.log_pk = log.id

    def process_response(self, request, response):
        log_pk = request.log_pk
        try:
            log = Log.objects.get(pk=log_pk)
            log.duration = datetime.timedelta( seconds=time.time() - request.start_time)
            log.save()
        except Exception as err:
            logger.error(str(err))
