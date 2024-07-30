from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.documents.models import Document
from src.documents.forms import DocumentFilterForm


def mgt_documents_example(request):
    return render(request, 'mgt/documents/list3.html')


def mgt_documents(request):
    form = DocumentFilterForm
    documents = Document.objects.all()

    documents_dict = DocumentSerializer(documents, many=True)

    context = {
        'form': form,
        'documents_dict': documents_dict,
    }
    return render(request, 'mgt/documents/list.html', context)

# def mgt_documents(request):
#     documents = Document.objects.all()

#     context = {
#         'documents': documents,
#         'products': None,
#         'customers': None,
#         'users': None,
#         'document_types': None,
#     }
#     return render(request, 'mgt/documents/list.html', context)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'number', 'cash_register', 'date', 'reference_document_number',
            'due_date', 'paid_status'
        ]


class DocumentListView(APIView):
    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


def get_document_dict(request):
    pass
