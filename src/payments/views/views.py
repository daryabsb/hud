from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from decimal import Decimal
from src.orders.models import PosOrder
from src.finances.models import PaymentType, Payment
from src.documents.models import Document, DocumentItem
from src.orders.models import get_order_statuses
from src.pos.utils import get_active_order, activate_order_and_deactivate_others
import uuid


@login_required
@require_POST
def save_pos_payment(request, order_number):
    try:
        with transaction.atomic():
            # Get the order
            order = get_object_or_404(PosOrder, number=order_number)
            
            # Collect payment amounts for each payment type
            payment_data = []
            total_paid = Decimal('0.00')
            
            for key, value in request.POST.items():
                if key.startswith('payment-amount-') and value:
                    try:
                        payment_type_id = key.replace('payment-amount-', '')
                        amount = Decimal(str(value).replace(',', ''))
                        if amount > 0:
                            payment_type = get_object_or_404(PaymentType, id=payment_type_id)
                            payment_data.append({
                                'payment_type': payment_type,
                                'amount': amount
                            })
                            total_paid += amount
                    except (ValueError, PaymentType.DoesNotExist):
                        continue
            
            if not payment_data:
                return JsonResponse({'error': 'No valid payment amounts provided'}, status=400)
            
            # Create document
            document = Document.objects.create(
                number=str(uuid.uuid4())[:8].upper(),
                user=request.user,
                customer=order.customer,
                cash_register=order.cash_register,
                order=order,
                document_type=order.document_type,
                warehouse=order.warehouse,
                total=order.total,
                paid_status=total_paid >= order.total
            )
            
            # Create document items from order items
            for order_item in order.order_items.all():
                DocumentItem.objects.create(
                    number=str(uuid.uuid4())[:8].upper(),
                    user=request.user,
                    document=document,
                    product=order_item.product,
                    quantity=order_item.quantity,
                    price=order_item.price,
                    discount=order_item.discount,
                    discount_type=order_item.discount_type
                )
            
            # Create payments
            for payment_info in payment_data:
                Payment.objects.create(
                    user=request.user,
                    document=document,
                    payment_type=payment_info['payment_type'],
                    amount=payment_info['amount']
                )
            
            # Update order status
            order.paid_status = total_paid >= order.total
            order.is_enabled = False
            order.save()
            
            # Activate next order in queue
            activate_order_and_deactivate_others(request.user)
            
            # Get updated active order for rendering
            active_order = get_active_order(request.user)
            
            # Prepare context for rendering
            from src.pos2.utils import get_payment_types
            from src.accounts.models import get_customers
            from src.configurations.models import get_menus
            
            context = {
                'active_order': active_order,
                'payment_types': get_payment_types(),
                'customers': get_customers(request.user),
                'menus': get_menus(request.user),
                'order_statuses': get_order_statuses(request.user),
            }
            
            return render(request, 'cotton/pos/pos.html', context)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
