import ast
from decimal import Decimal
from django.db.models import Q, F, Subquery, OuterRef
from django.views.generic import ListView
from django_filters.filterset import filterset_factory
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from src.documents.models import Document, DocumentItem, DocumentType
from src.orders.models import PosOrder, PosOrderItem
from src.accounts.models import Customer
# from src.documents.views import DocumentsTable
from src.documents.forms import DocumentFilterForm
from src.core.utils import get_fields, get_columns, get_indexes
from src.management.filters import DocumentFilterForm as DocumentFilter
from src.management.utils import apply_document_filters
from src.products.models import Product
from src.documents.forms import DocumentCreateForm, AddDocumentItem
from src.tax.models import Tax
from src.orders.forms import DocumentForm


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'number', 'cash_register', 'date', 'reference_document_number',
            'due_date', 'paid_status'
        ]


class ItemListView(ListView):
    model = Document
    template_name = 'mgt/documents/dumps/list4.html'

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

    return render(request, 'mgt/documents/dumps/list3.html', context)


def create_order_dict(request, Order: PosOrder, order_object=None) -> list:

    queryset = Order.objects.all().order_by('created')
    orders = []
    for order in queryset:
        form = DocumentForm(
            instance=order,
            initial={'document_type': order.document_type, 'user': request.user})
        order_dict = {
            'number': order.number,
            'items': order.items,
            'item_subtotal': order.item_subtotal,
            'total_tax': order.total_tax,
            'discounted_amount': order.discounted_amount,
            'total': order.total,
            'order': order,
            'form': form,
        }

        orders.append(order_dict)

        # if order_object:
        #     order_form = DocumentForm(
        #         instance=order_object,
        #         initial={'document_type': order_object.document_type, 'user': request.user})
        #     order_object_dict = {
        #         'number': order_object.number,
        #         'order': order_object,
        #         'form': order_form,
        #     }
        #     orders.append(order_object_dict)
    return orders


@login_required
def mgt_documents(request):
    filter = DocumentFilter(request.GET, queryset=Document.objects.all())
    document_form = DocumentFilter.form
    documents = Document.objects.all()
    orders_queryset = PosOrder.objects.filter(is_active=True)
    products = Product.objects.all()
    documents_dict = DocumentSerializer(documents, many=True)
    document_type = DocumentType.objects.first()

    orders = create_order_dict(request, PosOrder)

    context = {
        'filter': filter,
        'form': document_form,
        'orders': orders,
        'document_type': document_type,
        'products': products,
        'documents_dict': documents_dict,
    }

    return render(request, 'mgt/documents/list.html', context)


def mgt_add_new_order(request):
    document_type_id = request.POST.get('document-type')
    filter = DocumentFilter(request.GET, queryset=Document.objects.all())
    document_form = DocumentFilter.form
    documents = Document.objects.all()
    documents_dict = DocumentSerializer(documents, many=True)
    if document_type_id:
        document_type = get_object_or_404(DocumentType, id=document_type_id)
        order = PosOrder(user=request.user, document_type=document_type)
        order.save(doc_type=document_type.name.lower())
        products = Product.objects.all()
        orders = create_order_dict(request, PosOrder, order)

        context = {
            'filter': filter,
            'form': document_form,
            'documents_dict': documents_dict,
            'number': order.number,
            'orders': orders,
            'products': products,
            'document_type': document_type,
            'active_number': order.number,
            'active': 'show active'
        }
        return render(request, 'mgt/documents/add/new/render-new-document.html', context)


def add_document(request):
    return JsonResponse({"message": "Hiiiiiiiii"})


def documents_datatable_view(request):
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    search_value = request.GET.get("search[value]", None)
    # customer_search = request.GET['columns[3][search][value]']
    columns = get_columns('documents')
    fields = get_fields('documents')
    indexes = get_indexes('documents')
    # Prepare the initial queryset
    qs = Document.objects.select_related(
        'user', 'customer', 'cash_register', 'order', 'document_type', 'warehouse'
    ).annotate(
        user__name=F('user__name'),
        customer__name=F('customer__name'),
        cash_register__name=F('cash_register__name'),
        # order__id=F('order__id'),
        document_type__name=F('document_type__name'),
        warehouse__name=F('warehouse__name'),
    ).order_by("id")

    qs = apply_document_filters(request, qs)

    filtered_count = qs.count()
    qs = qs[start: start + length]

    data = list(qs.values(*get_fields('documents')))

    return JsonResponse({
        "recordsTotal": Document.objects.count(),
        "recordsFiltered": filtered_count,
        "draw": draw,
        "data": data,
        "columns": columns,
        "indexes": indexes,
    }, safe=False)


def documents_datatable_view2(request):
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    columns = get_columns('documents')
    fields = get_fields('documents')
    indexes = get_indexes('documents')

    # Prepare the initial queryset
    qs = Document.objects.select_related(
        'user', 'customer', 'cash_register', 'order', 'document_type', 'warehouse'
    ).annotate(
        user__name=F('user__name'),
        customer__name=F('customer__name'),
        cash_register__name=F('cash_register__name'),
        order__id=F('order__id'),
        document_type__name=F('document_type__name'),
        warehouse__name=F('warehouse__name'),
    ).order_by("id")

    # Apply the filters using DocumentFilterForm
    filter_set = DocumentFilter(request.GET, queryset=qs)

    qs = filter_set.queryset

    filtered_count = qs.count()
    qs = qs[start: start + length]

    data = list(qs.values(*get_fields('documents')))

    return JsonResponse({
        "recordsTotal": Document.objects.count(),
        "recordsFiltered": filtered_count,
        "draw": draw,
        "data": data,
        "columns": columns,
        "indexes": indexes,
    }, safe=False)


def mgt_documents2(request):
    # Instantiate the form with GET parameters to apply filters
    form = DocumentFilterForm(request.GET or None)

    # Apply the form's filters to the queryset
    documents = form.apply_filters(Document.objects.all())

    # Serialize the filtered queryset
    documents_dict = DocumentSerializer(documents, many=True).data

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


def add_document_items_to_document(request):

    product = None
    order = None
    form = AddDocumentItem(request.POST)
    product_id = request.POST.get('product', None)
    order_number = request.POST.get('order', None)

    if order_number:
        print('order number is: ', order_number)
        order = get_object_or_404(PosOrder, number=order_number)

    if product_id:
        product = get_object_or_404(Product, id=product_id)

        # Check if same item exists
        order_item = PosOrderItem.objects.filter(product=product).first()
        quantity = request.POST.get("quantity")
        if order_item:
            print('Order item exists!')
            order_item.quantity += int(quantity)
            order_item.save()
            print('Order_item_QUANTITY = ', order_item.quantity)
            context = {
                "product_id": product_id,
                # "item": order_item,
                "form": form,
                "order": order,
            }
            return render(request, "mgt/documents/add/new/render/render-item.html", context)
        else:

            price = request.POST.get("price")
            order_item = PosOrderItem(
                user=request.user,
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )
        order_item.save()

        # order_item = {
        #     "product": product,
        #     "quantity": request.POST.get("quantity"),
        #     "price": request.POST.get("price"),
        #     "price_before_tax": request.POST.get("price_before_tax"),
        #     "total": request.POST.get("total"),
        # }

        print(order_item.number)

        context = {
            "product_id": product_id,
            # "item": order_item,
            "form": form,
            "order": order,
        }

        return render(request, "mgt/documents/add/new/render/render-item.html", context)


def add_document_remove_items(request, item_number):
    order = None
    if item_number:
        item = get_object_or_404(PosOrderItem, number=item_number)

        if item:
            order = item.order
            item.delete()
        context = {
            "order": order,
        }
        return render(request, "mgt/documents/items/items-list.html", context)


def add_document_change_qty(request):

    product_id = request.GET.get('product', None)
    quantity = request.GET.get('quantity', 1)
    price_before_tax = request.GET.get('price_before_tax', 1)
    tax_id = request.GET.get('tax', None)
    # price = Decimal(quantity) * Decimal(request.GET.get('price', 1))
    price = Decimal(quantity) * Decimal(price_before_tax)
    discount_type = int(request.GET.get('discount_type', 0))
    discount = request.GET.get('discount', 0)
    total_before_tax = request.GET.get('total_before_tax', 0)
    total = request.GET.get('total', 1)
    order_number = request.GET.get('order', None)

    tax_cut = 0
    tax = None

    if tax_id:
        tax = Tax.objects.get(id=tax_id)
        if tax.is_fixed:
            tax_cut = tax.rate
        else:
            tax_cut = price * Decimal(tax.rate) / Decimal(100.00)

    print("order_number = ", order_number)
    discount_cut = 0
    if discount_type == 0:
        print(
            f"{price} X {Decimal(discount)} / 100 = { price * Decimal(discount) / 100 }")
        discount_cut = price * Decimal(discount) / 100
    elif discount_type == 1:
        discount_cut = Decimal(discount)

    if product_id:
        product = get_object_or_404(Product, id=product_id)

    total_before_tax = price - Decimal(discount_cut)
    total = total_before_tax + tax_cut

    form = AddDocumentItem(initial={
        'product': product.id,
        'quantity': quantity,
        'price_before_tax': product.price,
        'tax': tax,
        'price': price,
        'discount_type': discount_type,
        'discount': discount,
        'total_before_tax': total_before_tax,
        'total': total
    })

    # print('receive_product = ', product)
    # print('receive_quantity = ', quantity)
    # print('receive_price_before_tax = ', price_before_tax)
    # print('tax = ', tax)
    # print('receive_price = ', price)
    # print('receive_discount_type = ', discount_type)
    # print('receive_discount = ', discount)
    # print('receive_total_before_tax = ', total_before_tax)
    # print('receive_total = ', total)

    context = {
        'order_number': order_number,
        "form": form,
        "product": product,
    }
    return render(request, 'documents/mgt-forms/add/add-doc-item-form.html', context)
    # return JsonResponse({'message': 'documents/mgt-forms/add/add-doc-item-form.html'})


class DocumentListView(APIView):
    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


def get_document_dict(request):
    pass


QueryDict = {
    'datatables': ['1'],
    'draw': ['1'],
    'columns[0][data]': [''],
    'columns[0][name]': [''],
    'columns[0][searchable]': ['true'],
    'columns[0][orderable]': ['false'],
    'columns[0][search][value]': [''],
    'columns[0][search][regex]': ['false'],
    'columns[1][data]': ['id'],
    'columns[1][name]': [''],
    'columns[1][searchable]': ['true'],
    'columns[1][orderable]': ['false'],
    'columns[1][search][value]': [''],
    'columns[1][search][regex]': ['false'],
    'columns[2][data]': ['number'],
    'columns[2][name]': [''],
    'columns[2][searchable]': ['true'],
    'columns[2][orderable]': ['false'],
    'columns[2][search][value]': [''],
    'columns[2][search][regex]': ['false'],
    'columns[3][data]': ['customer__name'],
    'columns[3][name]': [''],
    'columns[3][searchable]': ['true'],
    'columns[3][orderable]': ['false'],
    'columns[3][search][value]': [''],
    'columns[3][search][regex]': ['false'],
    'columns[4][data]': ['cash_register__name'],
    'columns[4][name]': [''],
    'columns[4][searchable]': ['true'],
    'columns[4][orderable]': ['false'],
    'columns[4][search][value]': [''],
    'columns[4][search][regex]': ['false'],
    'columns[5][data]': ['order__id'],
    'columns[5][name]': [''],
    'columns[5][searchable]': ['true'],
    'columns[5][orderable]': ['false'],
    'columns[5][search][value]': [''],
    'columns[5][search][regex]': ['false'],
    'columns[6][data]': ['document_type__name'],
    'columns[6][name]': [''],
    'columns[6][searchable]': ['true'],
    'columns[6][orderable]': ['false'],
    'columns[6][search][value]': [''],
    'columns[6][search][regex]': ['false'],
    'columns[7][data]': ['warehouse__name'],
    'columns[7][name]': [''],
    'columns[7][searchable]': ['true'],
    'columns[7][orderable]': ['false'],
    'columns[7][search][value]': [''],
    'columns[7][search][regex]': ['false'],
    'columns[8][data]': ['date'],
    'columns[8][name]': [''],
    'columns[8][searchable]': ['true'],
    'columns[8][orderable]': ['false'],
    'columns[8][search][value]': [''],
    'columns[8][search][regex]': ['false'],
    'columns[9][data]': ['user__name'],
    'columns[9][name]': [''],
    'columns[9][searchable]': ['true'],
    'columns[9][orderable]': ['false'],
    'columns[9][search][value]': [''],
    'columns[9][search][regex]': ['false'],
    'columns[10][data]': ['reference_document_number'],
    'columns[10][name]': [''],
    'columns[10][searchable]': ['true'],
    'columns[10][orderable]': ['false'],
    'columns[10][search][value]': [''],
    'columns[10][search][regex]': ['false'],
    'columns[11][data]': ['internal_note'],
    'columns[11][name]': [''],
    'columns[11][searchable]': ['true'],
    'columns[11][orderable]': ['false'],
    'columns[11][search][value]': [''],
    'columns[11][search][regex]': ['false'],
    'columns[12][data]': ['note'],
    'columns[12][name]': [''],
    'columns[12][searchable]': ['true'],
    'columns[12][orderable]': ['false'],
    'columns[12][search][value]': [''],
    'columns[12][search][regex]': ['false'],
    'columns[13][data]': ['due_date'],
    'columns[13][name]': [''],
    'columns[13][searchable]': ['true'],
    'columns[13][orderable]': ['false'],
    'columns[13][search][value]': [''],
    'columns[13][search][regex]': ['false'],
    'columns[14][data]': ['discount'],
    'columns[14][name]': [''],
    'columns[14][searchable]': ['true'],
    'columns[14][orderable]': ['false'],
    'columns[14][search][value]': [''],
    'columns[14][search][regex]': ['false'],
    'columns[15][data]': ['discount_type'],
    'columns[15][name]': [''],
    'columns[15][searchable]': ['true'],
    'columns[15][orderable]': ['false'],
    'columns[15][search][value]': [''],
    'columns[15][search][regex]': ['false'],
    'columns[16][data]': ['discount_apply_rule'],
    'columns[16][name]': [''],
    'columns[16][searchable]': ['true'],
    'columns[16][orderable]': ['false'],
    'columns[16][search][value]': [''],
    'columns[16][search][regex]': ['false'],
    'columns[17][data]': ['paid_status'],
    'columns[17][name]': [''],
    'columns[17][searchable]': ['true'],
    'columns[17][orderable]': ['false'],
    'columns[17][search][value]': [''],
    'columns[17][search][regex]': ['false'],
    'columns[18][data]': ['stock_date'],
    'columns[18][name]': [''],
    'columns[18][searchable]': ['true'],
    'columns[18][orderable]': ['false'],
    'columns[18][search][value]': [''],
    'columns[18][search][regex]': ['false'],
    'columns[19][data]': ['total'],
    'columns[19][name]': [''],
    'columns[19][searchable]': ['true'],
    'columns[19][orderable]': ['false'],
    'columns[19][search][value]': [''],
    'columns[19][search][regex]': ['false'],
    'columns[20][data]': ['is_clocked_out'],
    'columns[20][name]': [''],
    'columns[20][searchable]': ['true'],
    'columns[20][orderable]': ['false'],
    'columns[20][search][value]': [''],
    'columns[20][search][regex]': ['false'],
    'columns[21][data]': ['created'],
    'columns[21][name]': [''],
    'columns[21][searchable]': ['true'],
    'columns[21][orderable]': ['false'],
    'columns[21][search][value]': [''],
    'columns[21][search][regex]': ['false'],
    'columns[22][data]': ['updated'],
    'columns[22][name]': [''],
    'columns[22][searchable]': ['true'],
    'columns[22][orderable]': ['false'],
    'columns[22][search][value]': [''],
    'columns[22][search][regex]': ['false'],
    'start': ['0'],
    'length': ['5'],
    'search[value]': [''],
    'search[regex]': ['false'],
    '_': ['1723182873596']
}
