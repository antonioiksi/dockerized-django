import json
import logging
import os
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.data_graph.models.GraphData import GraphData
from apps.data_graph.models.GraphModel import GraphModel
from apps.data_graph.views.GraphDataView import (GraphDataByModelNameView,
                                                 JsonbFilterView)

logger = logging.getLogger(__name__)


data1 = """
{"_id": "40001", "_type": "line", "_index": "shakespeare", "_score": 10.968148, "line_id": 40002, "speaker": "FRENCH KING", "play_name": "Henry V", "text_entry": "maiden walls that war hath never entered.", "line_number": "5.2.321", "speech_number": 67}
"""
data2 = """
{"_id": "4752", "_type": "line", "_index": "shakespeare", "_score": 10.873325, "line_id": 4753, "speaker": "JOAN LA PUCELLE", "play_name": "Henry VI Part 1", "text_entry": "Exeunt from the walls", "line_number": "", "speech_number": 27}
"""

class DataGraphModelsTest(TestCase):
    fixtures = [
        '00_user_test.json',
        '01_graph_test.json',
        '03_graph_model_drawing.json',
        '04_graph_model_test.json',
        '05_graph_data_test.json'
    ]
    """ Test module for Log model """

    #def setUp(self):
        #User.objects.create(username='antonio')
        #user = User.objects.get(username='antonio')

        #item1 = GraphData.objects.create( user=user, data=json.loads(data1))
        #item2 = GraphData.objects.create( user=user, data=json.loads(data2))


    def test_filter(self):
        user = User.objects.get(username='antonio')
        factory = APIRequestFactory()
        req = factory.get('/filter/')
        force_authenticate(req, user=user)
        view = JsonbFilterView.as_view()
        resp = view(req)

        pprint(json.dumps(resp.data))
        #all = GraphData.objects.all()
        #bin = Bin.objects.get(name='bin')
        #binItems = BinItem.objects.filter(bin=bin)
        #pprint([json.dumps(item) for item in GraphData.objects.all()])
        #index = 'shakespeare'
        #SQL_EXCLUDE = "SELECT true FROM data_graph_graphdata WHERE jsonfield::json->>'_index' = '%s'"
        #GraphData.objects.extra(where=[SQL_EXCLUDE % index]).get()
        self.assertEqual(1, 1)


    def test_GraphData(self):
        logger.info('sss')
        self.assertEqual(2, len(GraphData.objects.all()))


    def test_GraphObjects(self):
        self.assertEqual(3, len(GraphModel.objects.all()))


    def test_PersonObjects(self):
        person = GraphModel.objects.get(name='person')
        phone = GraphModel.objects.get(name='phone')
        persons = GraphData.objects.filter(data__has_keys=person.fields)
        phones = GraphData.objects.filter(data__has_keys=phone.fields)
        self.assertEqual(1, len(phones))


    def test_ObjectsByNameView(self):
        model_name = 'person'
        user = User.objects.get(username='antonio')
        factory = APIRequestFactory()
        req = factory.get('/objects-by-name/'+model_name)
        force_authenticate(req, user=user)
        view = GraphDataByModelNameView.as_view()
        resp = view(req, model_name=model_name)


        self.assertEqual(len(resp.data), 2)
        #self.assertEqual(resp.status_code, status.HTTP_200_OK)
