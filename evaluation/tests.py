from django.test import TestCase

# Create your tests here.

import unittest
from django.test import Client

from evaluation.models import Evaluation


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_get_evaluation(self):
        # Issue a GET request.
        response = self.client.get("/evaluations/")
        print(response.content)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

