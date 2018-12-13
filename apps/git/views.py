import logging
import subprocess

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth_jwt.permissions import PublicEndpoint
from backend import settings

logger = logging.getLogger(__name__)


class GitVersionView(APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        logger.debug('hello')
        try:
            version = subprocess.check_output(["git", "describe", "--tags"], cwd=settings.BASE_DIR).decode('utf-8')
            version = version.rstrip('\n')
        except Exception as err:
            logger.error(str(err))
            version = 'unknown version'

        return Response({'version': version})
