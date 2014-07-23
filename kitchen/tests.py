"""
This file is the test case for the Rewards.
"""
import json
from django.test import TestCase

from webhooks import webhook

import requests

class KitchenTests(TestCase):
    '''
    testing the reward
    '''

    def setUp(self):
        '''
        setup the enviroment
        '''
        # Create reward provider
        self.dataset = [{'output_data': {u'_shapes': u'{"objects":[{"type":"image","originX":"left","originY":"top","left":0,"top":0,"width":1250,"height":704,"fill":"rgb(0,0,0)","stroke":null,"strokeWidth":1,"strokeDashArray":null,"strokeLineCap":"butt","strokeLineJoin":"miter","strokeMiterLimit":10,"scaleX":1,"scaleY":1,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","src":"http://www.ucarecdn.com/0dfa9b79-ca93-4d38-a1fd-5b7cc8f02213/-/resize/600x/","filters":[],"crossOrigin":""},{"type":"polygon","originX":"left","originY":"top","left":338,"top":148,"width":1,"height":1,"fill":"green","stroke":"blue","strokeWidth":5,"strokeDashArray":null,"strokeLineCap":"butt","strokeLineJoin":"miter","strokeMiterLimit":10,"scaleX":1,"scaleY":1,"angle":0,"flipX":false,"flipY":false,"opacity":0.5,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","points":[{"x":-0.5,"y":-0.5},{"x":85,"y":-95},{"x":299,"y":-107},{"x":659,"y":-48},{"x":622,"y":282},{"x":297,"y":485},{"x":-2,"y":342}]}],"background":""}'}, 'score': 0.0, 'unit': 196, 'pk': 193}]
        self.webhook_url = 'http://localhost:8080/marble3d/judgements/receive/'

    def test_webhook(self):
        """
        Ensure that a a worker can buy something
        """
        headers = {'Content-type': 'application/json'}
        # send a request with json data and timeout of 2 seconds
        r = requests.post(self.webhook_url, data = json.dumps(self.dataset), headers = headers)
        print r

        

