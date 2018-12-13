import json
import logging
from pprint import pprint
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.utils.encoding import smart_str
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_bin.models import Bin
from apps.data_bin.views.BinItemDataView import BinItemDataView
from apps.report.views.ReportView import ReportViewSet

logger = logging.getLogger(__name__)

REPORT_TYPE_OPTIONS = ['word', 'excel']


class DataBinReportView(views.APIView):
    permission_classes = (PublicEndpoint,)

    def get(self, request, bin_id, report_type):
        user = self.request.user
        logger.info('%s %s' % (bin_id, report_type))

        if report_type not in REPORT_TYPE_OPTIONS:
            return Response({'status': 'error', 'message': 'wrong report_type: %s' + str(report_type)},
                            status=status.HTTP_400_BAD_REQUEST)

        bin = Bin.objects.get(id=bin_id)
        if bin is None:
            return Response({'status': 'error', 'message': 'bin not found: %s' + str(bin_id)},
                            status=status.HTTP_400_BAD_REQUEST)

        factory = APIRequestFactory()
        request = factory.get('/bin/%s/items/data/' % bin_id)
        force_authenticate(request, user=user)
        view = BinItemDataView.as_view()
        response = view(request, bin_pk=bin_id)

        if response.status_code == 400:
            logger.error('%s' % str(response.data))
            return Response({'status': 'error', 'message': '%s' % str(response.data)},
                            status=status.HTTP_400_BAD_REQUEST)

        bin_data = response.data
        # logger.info(str(bin_data))

        results = []
        results_dict = {}
        for row in bin_data:
            # index_name = row["_index"]
            # Do not remember for what purpose cutting alias, try to remove it
            # index_name = row["_aliase"][:30]
            index_name = row["_aliase"]
            if index_name not in results_dict.keys():
                results_dict[index_name] = []

            data = results_dict[index_name]
            data.append(row["_source"])
            # break

        for index_name in results_dict.keys():
            results.append({
                "index_name": index_name,
                "data": results_dict[index_name]
            })

        report_json = {
            "target": bin.name,
            "results": results,
            #     [
            #     {
            #         "index_name": "indexname1",
            #         "data": [
            #             {
            #                 "column1": "value1",
            #                 "column2": "value2"
            #             },
            #             {
            #                 "column1": "value1",
            #                 "column2": "value2"
            #             }
            #         ]
            #     },
            #     {
            #         "index_name": "indexname2",
            #         "data": [
            #             {
            #                 "column11": "value11",
            #                 "column21": "value21"
            #             }
            #         ]
            #     }
            # ]
        }

        # pprint(report_json)

        request = factory.post(path='/report/%s/data/' % report_type, data=json.dumps(report_json),
                               content_type='application/json')
        force_authenticate(request, user=user)
        view = ReportViewSet.as_view({'post': 'create'})
        response = view(request, type=report_type)
        logger.info(str(response.data))

        if 'path' in response.data:
            path = response.data['path']

            report_file = open(path, 'rb')
            # repoert_file_name = "корзинка_%s" % bin.name.replace(' ', '_')
            repoert_file_name = "korzinka_" + str(bin.id)
            logger.info(repoert_file_name)
            if report_type == 'excel':
                logger.info(repoert_file_name)
                response = HttpResponse(FileWrapper(report_file), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=' + repoert_file_name + '.xlsx'
            elif report_type == 'word':
                response = HttpResponse(FileWrapper(report_file), content_type='application/vnd.ms-word')
                response['Content-Disposition'] = 'attachment; filename=' + repoert_file_name + '.docx'

            return response
        else:
            return Response({'status': 'error', 'message': str(response.data)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response({'status': 'success', 'message': str(response.data)}, status=status.HTTP_200_OK)
