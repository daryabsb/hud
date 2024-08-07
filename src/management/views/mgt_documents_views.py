import ast
from django.db.models import Q, F, Subquery, OuterRef
from django.views.generic import ListView
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.documents.models import Document, DocumentItem
from src.documents.forms import DocumentFilterForm
from src.core.utils import get_fields, get_columns


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'number', 'cash_register', 'date', 'reference_document_number',
            'due_date', 'paid_status'
        ]


class ItemListView(ListView):
    model = Document
    template_name = 'mgt/documents/list4.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            draw = int(self.request.GET.get("draw", "1"))
            length = int(self.request.GET.get("length", "10"))
            start = int(self.request.GET.get("start", "0"))
            sv = self.request.GET.get("search[value]", None)
            qs = self.get_queryset().order_by("id")
            if sv:
                qs = qs.filter(
                    Q(id__icontains=sv)
                    | Q(document_type__name__icontains=sv)
                    | Q(warehouse__name__icontains=sv)
                    | Q(customer__name__icontains=sv)
                )
            filtered_count = qs.count()
            qs = qs[start: start + length]

            data = list(qs.values(
                'number',
                'customer__name',
                'document_type__name',
                'warehouse__name'
            ))

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": data,
                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


def get_document_data(request):
    print(request.GET)
    return JsonResponse({
        "draw": 1,
        "recordsTotal": 57,
        "recordsFiltered": 57,
        "data": [
            [
                "Airi",
                "Satou",
                "Accountant",
                "Tokyo",
                "28th Nov 08",
                "$162,700"
            ],
            [
                "Angelica",
                "Ramos",
                "Chief Executive Officer (CEO)",
                "London",
                "9th Oct 09",
                "$1,200,000"
            ],
            [
                "Ashton",
                "Cox",
                "Junior Technical Author",
                "San Francisco",
                "12th Jan 09",
                "$86,000"
            ],
            [
                "Bradley",
                "Greer",
                "Software Engineer",
                "London",
                "13th Oct 12",
                "$132,000"
            ],
            [
                "Brenden",
                "Wagner",
                "Software Engineer",
                "San Francisco",
                "7th Jun 11",
                "$206,850"
            ],
            [
                "Brielle",
                "Williamson",
                "Integration Specialist",
                "New York",
                "2nd Dec 12",
                "$372,000"
            ],
            [
                "Bruno",
                "Nash",
                "Software Engineer",
                "London",
                "3rd May 11",
                "$163,500"
            ],
            [
                "Caesar",
                "Vance",
                "Pre-Sales Support",
                "New York",
                "12th Dec 11",
                "$106,450"
            ],
            [
                "Cara",
                "Stevens",
                "Sales Assistant",
                "New York",
                "6th Dec 11",
                "$145,600"
            ],
            [
                "Cedric",
                "Kelly",
                "Senior Javascript Developer",
                "Edinburgh",
                "29th Mar 12",
                "$433,060"
            ]
        ]
    })


def mgt_documents_example(request):
    form = DocumentFilterForm
    documents = Document.objects.all()
    documents_dict = DocumentSerializer(documents, many=True)
    context = {
        'form': form,
        'documents': documents_dict,
    }
    print(request.GET)

    return render(request, 'mgt/documents/list3.html', context)


def documents_datatable_view(request):
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    search_value = request.GET.get("search[value]", None)

    qs = Document.objects.select_related(
        'user', 'customer', 'cash_register', 'order', 'document_type', 'warehouse'
    ).annotate(
        user__name=F('user__name'),
        customer__name=F('customer__name'),
        cash_register__name=F('cash_register__name'),
        order__id=F('order__id'),
        document_type__name=F('document_type__name'),
        warehouse__name=F('warehouse__name'),
        # image_url=F('image__url'),
    ).order_by("id")

    if search_value:
        try:
        # Convert the string 'True' or 'False' to a boolean
            paid_dtatus_query = ast.literal_eval(search_value)
        except (ValueError, SyntaxError):
            paid_dtatus_query = None
        # Create a subquery to filter DocumentItem based on product name
        # qs = Q
        # document_items_subquery = DocumentItem.objects.filter(
        #     document=OuterRef('pk'),
        #     product__iexact=int(search_value)
        # ).values('document')
        print('doc_type is: ', search_value)
        qs = qs.filter(
            # Q(name__icontains=search_value)
            # Q(document_items__product__name__icontains=search_value)
            # Q(number__icontains=search_value)
            Q(document_type__id__exact=int(search_value))
            | Q(paid_status__exact=paid_dtatus_query)
            # | Q(document_type__name__icontains=search_value)
            # | Q(user__name__icontains=search_value)
            # | Q(reference_document_number__icontains=search_value)
            # | Q(internal_note__icontains=search_value)
            # | Q(stock_date__icontains=search_value)
            # | Q(created__icontains=search_value)
            # | Q(order__name__icontains=search_value)
            # | Q(customer__name__icontains=search_value)
            # | Q(cash_register__name__icontains=search_value)
            # | Q(warehouse__name__icontains=search_value)
            # | Q(id__in=Subquery(document_items_subquery))

        )

    filtered_count = qs.count()
    qs = qs[start: start + length]

    data = list(qs.values(*get_fields('documents')))
    columns = get_columns('documents')
    return JsonResponse({
        "recordsTotal": Document.objects.count(),
        "recordsFiltered": filtered_count,
        "draw": draw,
        "data": data,
        "columns": columns,
    }, safe=False)


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


class DocumentListView(APIView):
    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


def get_document_dict(request):
    pass
