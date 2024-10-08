from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from src.printers.pdf.fpdf import MyPDF
from src.products.models import Product




def export_pdf(request):
    user = request.user
    queryset = Product.objects.select_related('parent_group', 'barcode').values_list("id", "name", "parent_group__name", "barcode__value", "price")
    table_header = [
        {"text": "ID", "align": "left", "width": 10},
        {"text": "NAME", "align": "left", "width": 25},
        {"text": "PARENT", "align": "left", "width": 20},
        {"text": "BARCODE", "align": "left", "width": 25},
        {"text": "PRICE", "align": "left", "width": 20}
    ]
    table_name = 'PRODUCT LIST'
    fpdf_kwargs = {
        "format": 'A4',
        "orientation": 'landscape'
    }
    pdf = MyPDF(user=user, queryset=queryset, table_name=table_name, table_header=table_header, **fpdf_kwargs)

    return HttpResponse(bytes(pdf.output()), content_type="application/pdf")