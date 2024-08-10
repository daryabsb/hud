from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from src.documents.models import Document
# Create your views here.

from table import Table
from table.columns import Column

class DocumentsTable(Table):

    number = Column(field='number')
    # customer = Column(field='customer__name')

    class Meta:
        model = Document
        ajax = True
        ajax_source = reverse_lazy('document_table_data_load')

from table.views import FeedDataView

class MyDataView(FeedDataView):

    token = DocumentsTable.token

    def get_queryset(self):
        return Document.objects.all()