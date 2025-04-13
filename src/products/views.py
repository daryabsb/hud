from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q, F
from src.products.models import Product
from src.products.utils import apply_product_filters
from src.core.utils import get_fields, get_columns, get_searchable_fields
from django.http import JsonResponse
from django.apps import apps

# Create your views here.


def documents_datatable_view(request):
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    search_value = request.GET.get("search[value]", None)
    # customer_search = request.GET['columns[3][search][value]']
    columns = get_columns('products')
    fields = get_fields('products')
    indexes = get_indexes('products')
    # Prepare the initial queryset
    qs = Product.objects.select_related(
        'user', 'parent_group', 'currency', 'barcode', 'document_type',
    ).annotate(
        user__name=F('user__name'),
        parent_group__name=F('parent_group__name'),
        currency__name=F('currency__name'),
        # order__id=F('order__id'),
        barcode__value=F('barcode__value'),
    ).order_by("id")

    qs = apply_product_filters(request, qs)

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


products_fields = ['id', 'name', 'image', 'barcode',
                   'parent_group', 'price', 'user', 'currency']


def get_app(model):
    app_names = {
        'product': 'products',
        'productgroup': 'products',
        'document': 'documents',
        'documentitem': 'documents',
        'posorder': 'orders',
        'posorderitem': 'orders',
    }

    return app_names[model]


def product_search_datatable(request, app_name=None, model=None):
    # Extract DataTables parameters
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    search_value = request.GET.get("search[value]", None)

    # Initialize response data
    response = {
        "recordsTotal": 0,
        "recordsFiltered": 0,
        "draw": draw,
        "data": [],
        "columns": [],
    }

    # Handle model loading
    if not model:
        return JsonResponse({**response, "error": "No model provided"}, safe=False)
    try:
        model_name = model.lower()
        ModelClass = apps.get_model(app_label=app_name, model_name=model_name)
    except (LookupError, ImproperlyConfigured) as e:
        return JsonResponse({**response, "error": f"Invalid model: {model_name}"}, safe=False)

    qs = ModelClass.objects.none()

    # fields = get_fields(app_name)
    # columns = get_columns(app_name)
    fields, columns, indexes = get_searchable_fields(app_name)

    if search_value:
        qs = ModelClass.objects.filter_by_search_value(search_value)

    # Get counts
    filtered_count = qs.count()
    total_count = ModelClass.objects.count()

    # Apply pagination
    qs = qs[start:start + length]

    # Get fields and columns using manager methods

    # Convert queryset to list of dictionaries
    data = list(qs.values(*fields))

    # Return JSON response
    return JsonResponse({
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "draw": draw,
        "data": data,
        "columns": columns,
    }, safe=False)


def search_datatable_view(request, model=None):
    from src.core.utils import get_searchable_fields
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    search_value = request.GET.get("search[value]", None)

    app_name = None
    model_name = None

    try:
        app_name = get_app(model)
        model_name = apps.get_model(app_name, model)

    except Exception as e:
        print('Model must be provided! ', e)

    if not model_name or not app_name:
        raise "something is wrong"

    qs = model_name.objects.none()

    if search_value:
        qs = Product.objects.select_related('currency', 'barcode').annotate(
            user__name=F('user__name'),
            barcode__value=F('barcode__value'),
            parent_group__name=F('parent_group__name'),
            currency__name=F('currency__name'),
            # image_url=F('image__url'),
        ).order_by("id").filter(
            # qs = qs
            Q(name__icontains=search_value)
            | Q(code__icontains=search_value)
            | Q(barcode__value__icontains=search_value)
            | Q(parent_group__name__icontains=search_value)
            | Q(description__icontains=search_value)
        )

    filtered_count = qs.count()
    qs = qs[start: start + length]

    # if qs is not None:
    fields, columns, _ = get_searchable_fields('products')

    data = list(qs.values(*fields))

    return JsonResponse({
        "recordsTotal": Product.objects.count(),
        "recordsFiltered": filtered_count,
        "draw": draw,
        "data": data,
        "columns": columns,
    }, safe=False)
