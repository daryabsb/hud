import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from project.fundreport.utils import create_fund_report
from project.fundreport.models import Fund, FundValue, IndexValue

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--fund',
            action='store',
            dest='fund_id',
            help = 'Please provide a numeric id for the fund for which you want to generate a command',
    )
    
    def handle(self, app_name=None, target=None, **options):
        try:
            fund_id = options.get('fund_id', None)
            Fund.objects.get(id=(fund_id))
        except Fund.DoesNotExist:
            raise CommandError('Fund id fund_id does not exist')
        except Exception:
            raise CommandError('please provide a fund id')
        ids = []

        if fund_id == 'ALL':
            for fund in Fund.objects.all():
                ids.append(fund.id)
        else:
            ids.append(int(fund_id))


        for id in ids:
            'create files named fund_001.pdf, fund_002.pdf etc in current directory'
            if settings.TESTING:
                outfilename = os.path.abspath(os.path.join(settings.PDF_OUT_DIR, "test_fund_%03d.pdf" % id))
            else:
                outfilename = os.path.abspath(os.path.join(settings.PDF_OUT_DIR, "fund_%03d.pdf" % id))
            if not os.path.isdir(settings.PDF_OUT_DIR):
                os.makedirs(settings.PDF_OUT_DIR)
            rawpdf = create_fund_report(id)
            open(outfilename, 'wb').write(rawpdf)
            print ('Created', outfilename)
        

