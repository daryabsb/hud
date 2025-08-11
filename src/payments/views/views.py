from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def save_pos_payment(request, order_number):

    amount = request.POST.getlist('payment-amount', None)


    if amount:
        print(f'An amount of {amount} payed for {order_number}')
        return JsonResponse({'success': True})
    return JsonResponse({'failed': False})
