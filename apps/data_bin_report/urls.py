from django.conf.urls import url

from apps.data_bin_report.views import DataBinReportView

urlpatterns = [

    url(r'^data-bin-report/(?P<bin_id>(\d+))/(?P<report_type>(.+))$', DataBinReportView.as_view(), name='data-bin-report'),

]
