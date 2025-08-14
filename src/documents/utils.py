

from src.documents.models import Document, DocumentType
from src.pos.models import CashRegister
from src.orders.models import PosOrder
from django.db import transaction

from django.utils import timezone
from datetime import timedelta


from django.utils import timezone
from datetime import timedelta


def get_due_date():
    return 15


def create_document_from_order(order: PosOrder) -> Document:
    """
    Utility function to create a Document instance from a PosOrder instance.

    Args:
        order: PosOrder instance

    Returns:
        Document: Newly created Document instance

    Raises:
        ValueError: If required fields are missing or invalid
    """
    with transaction.atomic():
        # If the order is active, activate the next available order before saving
        if order.is_active:
            next_order: PosOrder = (
                PosOrder.objects
                .filter(user=order.user, is_enabled=True, is_active=False)
                .exclude(pk=order.pk)
                .order_by("-created")  # Or another ordering criterion
                .first()
            )
            if next_order:
                next_order.is_active = True
                next_order.save()
    # Generate reference document number if not provided
    reference_doc_number = order.reference_document_number or f"REF-{order.number}"

    # Calculate due date as days from order date
    due_date_days = (order.due_date -
                     order.date).days if order.due_date else get_due_date()

    # Map discount_apply_rule (assuming default mapping, adjust as needed)
    discount_apply_rule = 0  # Default value, modify based on your business logic

    # Create and save the document
    document: Document = Document.objects.create(
        user=order.user,
        customer=order.customer,
        cash_register=order.cash_register,
        order=order.number,  # Using order number as the order field
        document_type=order.document_type,
        warehouse=order.warehouse,
        date=order.date,
        reference_document_number=order.number,
        internal_note=order.internal_note,
        note=order.note,
        due_date=due_date_days,
        discount=int(order.discount),  # Convert float to int
        discount_type=int(order.discount_type),  # Convert float to int
        discount_apply_rule=discount_apply_rule,
        paid_status=order.paid_status,
        total=float(order.total),  # Convert Decimal to float
        is_clocked_out=not order.is_active  # Map is_active to is_clocked_out
    )

    order.reference_document_number = document.number
    order.is_enabled = False
    order.save()

    return document


def create_document(
    number: str,
    user,
    document_type,
    warehouse,
    reference_document_number: str,
    customer=None,
    cash_register=None,
    order: str = None,
    date=None,
    internal_note: str = None,
    note: str = None,
    due_date_days: int = None,
    discount: int = 0,
    discount_type: int = 0,
    discount_apply_rule: int = 0,
    paid_status: bool = False,
    total: float = 0.0,
    is_clocked_out: bool = False
):
    """
    Utility function to create a new Document instance.

    Args:
        number (str): Unique document number
        user: User instance (required)
        document_type: DocumentType instance (required)
        warehouse: Warehouse instance (required)
        reference_document_number (str): Unique reference document number
        customer: Customer instance (optional)
        cash_register: CashRegister instance (optional)
        order (str, optional): Order identifier
        date (datetime, optional): Document date, defaults to current time
        internal_note (str, optional): Internal note
        note (str, optional): Public note
        due_date_days (int, optional): Days until due date, uses default if None
        discount (int): Discount amount, defaults to 0
        discount_type (int): Discount type, defaults to 0
        discount_apply_rule (int): Discount application rule, defaults to 0
        paid_status (bool): Payment status, defaults to False
        total (float): Document total, defaults to 0.0
        is_clocked_out (bool): Clock out status, defaults to False

    Returns:
        Document: Newly created Document instance

    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Validate required fields
    if not number:
        raise ValueError("Document number is required")
    if not user:
        raise ValueError("User is required")
    if not document_type:
        raise ValueError("Document type is required")
    if not warehouse:
        raise ValueError("Warehouse is required")
    if not reference_document_number:
        raise ValueError("Reference document number is required")

    # Set default date if not provided
    document_date = date or timezone.now()

    # Calculate due date if due_date_days is provided
    if due_date_days is not None:
        due_date = due_date_days
    else:
        due_date = get_due_date()  # Assuming get_due_date is defined elsewhere

    # Create and save the document
    document = Document.objects.create(
        number=number,
        user=user,
        customer=customer,
        cash_register=cash_register,
        order=order,
        document_type=document_type,
        warehouse=warehouse,
        date=document_date,
        reference_document_number=reference_document_number,
        internal_note=internal_note,
        note=note,
        due_date=due_date,
        discount=discount,
        discount_type=discount_type,
        discount_apply_rule=discount_apply_rule,
        paid_status=paid_status,
        total=total,
        is_clocked_out=is_clocked_out
    )

    return document
