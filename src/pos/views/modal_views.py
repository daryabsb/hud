
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from src.products.models import Product
from src.orders.models import PosOrder, PosOrderItem


def modal_product(request, id):
    active_order = PosOrder.objects.filter(is_active=True).first()
    product = get_object_or_404(Product, id=id)

    if product:
        context = {"product": product, "active_order": active_order}
        return render(request, 'pos/modals/product-modal.html', context)


def modal_calculator(request):
    import json
    is_ajax = request.GET.get('is_ajax', False)
    div_class = request.GET.get('div-class', '')
    el_id = request.GET.get('el-id', '')
    url = request.GET.get('url', '')
    template_name = request.GET.get('template-name', '')
    digits = [[7, 8, 9, '/'], [4, 5, 6, '*'],
              [1, 2, 3, '-'], [0, '.', '=', '+'],]
    context = {
        "is_ajax": is_ajax,
        "div_class": div_class,
        "el_id": el_id,
        "template_name": template_name,
        "url": url,
        "digits": digits,
    }

    return render(request, 'hud/pos/modals/calculator-modal.html', context)


def calculate(request):
    from django.http import JsonResponse
    calculation = request.POST.get('display', '')
    # Process the calculation as needed, e.g., log it, store it, etc.
    print("calculation = ", calculation)
    return JsonResponse({'message': calculation})


def add_digit(request):
    if request.method == 'POST':
        current_value = request.POST.get('display', '')
        digit = request.POST.get('digit', '')
        new_value = current_value + digit
        return render(request, 'hud/pos/buttons/input_display.html', {'new_value': new_value})
    return render(request, 'keypad.html', {'error': 'Invalid request'})
