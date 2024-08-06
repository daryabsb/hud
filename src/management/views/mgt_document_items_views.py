from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from src.documents.models import Document, DocumentItem
from src.core.utils import get_fields, get_columns


def document_items_datatable_view(request):
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    search_value = request.GET.get("search[value]", None)
    document_id = request.GET.get('document-id', None)

    document = None
    if document_id:
        document = get_object_or_404(Document, id=int(document_id))

    print('doc_id = ', document_id)

    qs = DocumentItem.objects.filter(
        document=document
    ).select_related(
        'user', 'document', 'product'
    ).annotate(
        user__name=F('user__name'),
        product__name=F('product__name'),
        document__id=F('document__id')
        # image_url=F('image__url'),
    ).order_by("id")

    if search_value:
        qs = qs.filter(
            Q(Q(product__exact=int(search_value)))
            # | Q(document__in=search_value)
            | Q(product__name__icontains=search_value)
            # | Q(product__exact=int(search_value))
            # | Q(product__parent_group__name__icontains=search_value)
            # | Q(product__parent_group__exact=int(search_value))
            # | Q(price__icontains=search_value)
            # | Q(returned__icontains=search_value)
            # | Q(created__gte=search_value)
            # | Q(created__lte=search_value)
        )

    filtered_count = qs.count()
    qs = qs[start: start + length]

    data = list(qs.values(*get_fields('document_items')))
    columns = get_columns('document_items')
    return JsonResponse({
        "recordsTotal": Document.objects.count(),
        "recordsFiltered": filtered_count,
        "draw": draw,
        "data": data,
        "columns": columns,
    }, safe=False)
