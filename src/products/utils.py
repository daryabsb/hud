

def apply_product_filters(request, qs):
    from src.core.utils import get_indexes
    from django.db.models import Q
    from src.accounts.models import Customer, Warehouse
    from src.documents.models import DocumentType
    from src.pos.models import CashRegister
    from src.products.models import Product
    from datetime import datetime
    from django.utils.timezone import now, make_aware

    indexes = get_indexes('documents')

    # Customer
    product_search_value = request.GET.get(
        f"columns[{indexes['product']}][search][value]", None)
    if product_search_value:
        print("product_search_value = ", product_search_value)
        product = Product.objects.get(id=int(product_search_value))
        qs = qs.filter(document_items__product=product).distinct()

    # Customer
    customer_search_value = request.GET.get(
        f"columns[{indexes['customer']}][search][value]", None)
    if customer_search_value:
        customer = Customer.objects.get(id=int(customer_search_value))
        qs = qs.filter(Q(customer=customer))

    # Document Type
    document_type_search_value = request.GET.get(
        f"columns[{indexes['document_type']}][search][value]", None)
    if document_type_search_value:
        document_type = DocumentType.objects.get(
            id=int(document_type_search_value))
        qs = qs.filter(Q(document_type=document_type))

    # Cash Register
    cash_register_search_value = request.GET.get(
        f"columns[{indexes['cash_register']}][search][value]", None)
    if cash_register_search_value:
        cash_register = CashRegister.objects.get(
            number=cash_register_search_value)
        qs = qs.filter(Q(cash_register=cash_register))

    # Warehouse
    warehouse_search_value = request.GET.get(
        f"columns[{indexes['warehouse']}][search][value]", None)
    if warehouse_search_value:
        warehouse = Warehouse.objects.get(
            id=int(warehouse_search_value))
        qs = qs.filter(Q(warehouse=warehouse))

    # Paid status
    paid_status_search_value = request.GET.get(
        f"columns[{indexes['paid_status']}][search][value]", None)
    if paid_status_search_value:
        qs = qs.filter(Q(paid_status=paid_status_search_value))

    # Document Reference Number
    doc_ref_num_search_value = request.GET.get(
        f"columns[{indexes['reference_document_number']}][search][value]", None)
    if doc_ref_num_search_value:
        qs = qs.filter(
            Q(reference_document_number__icontains=doc_ref_num_search_value))

    created_start_value = request.GET.get(
        f"columns[{indexes['start_date']}][search][value]", None)

    if created_start_value:
        print("created_start_value = ", created_start_value)
        start_date = make_aware(datetime.strptime(
            f"{created_start_value} 00:00:00", '%Y-%m-%d %H:%M:%S'))
        qs = qs.filter(Q(created__gte=start_date))

    created_end_value = request.GET.get(
        f"columns[{indexes['end_date']}][search][value]", None)
    if created_end_value:
        end_date = make_aware(datetime.strptime(
            f"{created_end_value} 23:59:59", '%Y-%m-%d %H:%M:%S'))
        qs = qs.filter(Q(created__lte=end_date))
    else:
        end_date = now()
        qs = qs.filter(Q(created__lte=end_date))

    return qs
