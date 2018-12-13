import json
import os
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.data_graph.views.GraphNodeView import GraphNodesByModelsView


class GraphNodeViewTest(TestCase):
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


    def test_get_save(self):
        user = User.objects.get(username='antonio')
        factory = APIRequestFactory()

        req1 = factory.post('/node/save/graph01',['person','phone'], format='json')
        force_authenticate(req1, user=user)
        view1 = GraphNodesByModelsView.as_view()
        resp1 = view1(req1, action='save',  graph_name='graph01')
        pprint(resp1.data)

        req2 = factory.post('/node/get/graph01/',['person','phone'], format='json')
        force_authenticate(req2, user=user)
        view2 = GraphNodesByModelsView.as_view()
        resp2 = view2(req2, action='get',  graph_name='graph01')
        pprint(resp2.data)

        self.assertEqual(resp1.data[0], len(resp2.data))
