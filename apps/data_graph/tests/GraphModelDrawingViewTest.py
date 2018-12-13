import json
import os
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.data_graph.views.GraphModelDrawingView import \
    GraphModelDrawingViewSet
from apps.data_graph.views.GraphNodeView import GraphNodesByModelsView


class GraphModelDrawingViewTest(TestCase):
    fixtures = [
        '00_user_test.json',
        '01_graph_test.json',
        '03_graph_model_drawing.json',
        '04_graph_model_test.json',
        '05_graph_data_test.json'
    ]

    #def setUp(self):
        # this executes after fixtures!!!
        #User.objects.create(username='antonio')
        #user = User.objects.get(username='antonio')
        #User.objects.create(username='user')
        #user2 = User.objects.get(username='antonio')

        #item1 = GraphData.objects.create( user=user, data=json.loads(data1))
        #item2 = GraphData.objects.create( user=user, data=json.loads(data2))


    def test_list(self):
        user = User.objects.get(username='antonio')
        factory = APIRequestFactory()

        req = factory.get('/graph/drawing/')
        force_authenticate(req, user=user)
        view = GraphModelDrawingViewSet.as_view({'get': 'list'})
        resp = view(req)
        pprint(resp.data)
        self.assertEqual(1, 1)
