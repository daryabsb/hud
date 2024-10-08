from django.http import HttpResponse
from django.shortcuts import render
from src.finances.models import Fund
# Create your views here.
from src.management.utils import generate_invoice


def index(request):
    context = {}
    context['funds'] = Fund.objects.all()
    return render(request, 'finance/index.html', context)


def fundreport(request, id):
    # Create a PDF for the fund and return as HTTP Response

    # All the work is done in a separate function, so we can
    # call it from background commands as well as web requests.
    fund = Fund.objects.get(id=id)
    pdf = generate_invoice(fund.id)

    response = HttpResponse(pdf, content_type="application/pdf")

    # note that 'inline' will bring up the PDF in a browser tab in most
    # modern browsers; changing this to 'attachment' will prompt it to
    # be downloaded to the desktop.  The choice is yours.
    response['Content-Disposition'] = 'inline; filename="fund_report.pdf"'
    return response
