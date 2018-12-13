import logging
import os
import time

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.auth_jwt.permissions import PublicEndpoint
from apps.report.generators.excel import makeexcel
from apps.report.generators.word import makedocx
from apps.report.serializers.ReportSerializer import ReportSerializer
from backend import settings

logger = logging.getLogger(__name__)

class ReportViewSet(viewsets.ViewSet):

    permission_classes = (PublicEndpoint,)
    # permission_classes = (permissions.IsAuthenticated,) # TODO не работает в data_bin_report
    # authentication_classes = (JWTAuthentication,)
    serializer_class = ReportSerializer

    def create(self, request, type):
        file_format = {"word": "docx", "excel": "xlsx"}

        try:
            serializer = ReportSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            dir_name = settings.REPORTS_DIR + time.strftime("%Y/%m/%d/", time.gmtime())
            file_name = round(time.time()).__str__() + "." + file_format.get(type, "tmp")
            file_path = dir_name + file_name
            os.makedirs(dir_name, exist_ok=True)
            with open(file_path, "wb+") as report:
                if type == "word":
                    doc = makedocx(serializer.initial_data)
                elif type == "excel":
                    doc = makeexcel(serializer.initial_data)
                else:
                    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
                report.write(doc)
        except Exception as e:
            logger.error(str(e))
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "success", "path": file_path}, status=status.HTTP_201_CREATED)
