from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings

import os

from project.fundreport.models import Fund


class FundReportTestCases(TestCase):
    
    fixtures = ['initial_data.json', ]
    
    def test_demo(self):
        self.assertEqual(2+2, 4, 'something is up')

    def test_web_report(self):
        "Check the URL creates a PDF"
        response = self.client.get('/fundreport/1.pdf')
        self.assertEqual(response.status_code, 200)
        startOfFile = response.content[0:8]
        self.assertEqual(startOfFile, b'%PDF-1.4', 'unexpected content in response: %s' % startOfFile)

    def test_command_tier1report(self):
        "Check our command creates the file in the current directory"
        from django.core.management import call_command
        tests_out_filepath = settings.PDF_OUT_DIR
        if not os.path.isdir(tests_out_filepath):
            os.makedirs(tests_out_filepath)
        filepath = os.path.abspath(os.path.join(tests_out_filepath, "test_fund_001.pdf"))
        if os.path.isfile(filepath):
            os.remove(filepath)
        call_command('makepdf', '--fund', 1)
        with open(filepath, 'rb') as pdf:
            pdfdata = pdf.read()[0:8]
        self.assertEqual(pdfdata, b'%PDF-1.4')
