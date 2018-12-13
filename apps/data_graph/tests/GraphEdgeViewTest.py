import json
import os
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.data_graph.models.Graph import GraphModel
from apps.data_graph.models.GraphData import GraphData
from apps.data_graph.views.GraphDataView import (GraphDataByModelNameView,
                                                 JsonbFilterView)
from apps.data_graph.views.GraphNodeEdgeView import GraphEdgesByRelationsView


class GraphEdgeViewTest(TestCase):
    fixtures = [
        '00_user_test.json',
        '01_graph_test.json',
        '03_graph_model_drawing.json',
        '04_graph_model_test.json',
        '05_graph_data_test.json',
        '06_graph_relation_test.json',
        '07_graph_node_test.json'
    ]

    #def setUp(self):
        #User.objects.create(username='antonio')

    def test_GraphEdgesByRelationsView(self):
        user = User.objects.get(username='antonio')
        factory = APIRequestFactory()
        req = factory.post('/edge/graph01',['call_to','same_index_type'], format='json')
        force_authenticate(req, user=user)
        view = GraphEdgesByRelationsView.as_view()
        resp = view(req, graph_name='graph01')

        pprint(json.dumps(resp.data))
        self.assertEqual(resp.HTTP_200_OK, status.HTTP_200_OK)
