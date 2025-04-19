from django.shortcuts import render
from collections import defaultdict

from src.orders.models import PosOrder
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from django.contrib.auth.decorators import login_required
from src.configurations.models import ApplicationProperty
# Create your views here.
from src.accounts.models import Customer
from src.accounts.forms import CustomerFieldForm


def prepare_products_variannts(queryset=None):
    from src.products.models import Product, ProductGroup
    if not queryset:
        queryset = Product.objects.all()

        grouped_products = defaultdict(lambda: defaultdict(list))

        for product in products:

            grouped_products[product.brand][product.name].append({
                'size': product.size,
                'dietary_option': product.dietary_option,
                'price': product.price,
                'stock': product.stock,
            })


@login_required
def pos_home(request, number=None):
    from src.orders.utils import context_factory
    layout_object = ApplicationProperty.objects.get(name='layout')

    # extra querysets
    # customers = Customer.objects.all()
    # customer_form = CustomerFieldForm(
    #     customer=active_order.customer)

    context = context_factory(
        ["active_order", "orders", "payment_types", "payment_type", "menus"], context={'initialized': True})

    if layout_object.value == 'visual':
        context = context_factory(['products', 'groups'], context)
        return render(request, 'cotton/pos_base/visual/index.html', context)

    return render(request, 'cotton/pos_base/standard/index.html', context)


# class PosHomeView(LoginRequiredMixin, View):
#     template_name_standard = 'cotton/pos_base/standard/index.html'
#     template_name_visual = 'cotton/pos_base/visual/index.html'

#     def get_template_for_view(self):
#         layout = ApplicationProperty.objects.get(name='layout')
#         return self.template_name_visual if layout.value == 'visual' else self.template_name_standard

#     def get_context_data(self, user, active_order=None):
#         layout = ApplicationProperty.objects.get(name='layout')
#         pos_orders = PosOrder.objects.all()
#         payment_types = PaymentType.objects.filter(is_enabled=True)

#         context = {
#             "active_order": active_order or get_active_order(),
#             "orders": pos_orders,
#             "payment_types": payment_types,
#             "payment_type": payment_types.first(),
#         }

#         if layout.value == 'visual':
#             context["products"] = Product.objects.all()
#             context["groups"] = ProductGroup.objects.filter(
#                 parent__isnull=True)

#         return context

#     def get(self, request, number=None):
#         print('Last Activity: ', request.session.get('last_activity'))
#         context = self.get_context_data(request.user)
#         return render(request, self.get_template_for_view(), context)

#     def post(self, request):
#         """
#         Handle adding a new order (HTMX).
#         """
#         template = self.get_template_for_view()
#         order = create_new_order(request.user)
#         active_order = aod(request.user, order_number=order.number)

#         context = {"order": active_order, "active_order": active_order}
#         return render(request, template, context)

#     def delete(self, request):
#         """
#         Handle deleting the active order (HTMX).
#         """
#         template = self.get_template_for_view()
#         active_order = get_active_order()
#         active_order.delete()
#         aod(request.user, activate=True)

#         context = {"order": active_order, "active_order": active_order}
#         return render(request, template, context)

#     def http_method_not_allowed(self, request, *args, **kwargs):
#         # HTMX sends DELETE as POST + `HX-Method`
#         if request.headers.get("HX-Request") and request.POST.get("_method") == "DELETE":
#             return self.delete(request)
#         return HttpResponseNotAllowed(['GET', 'POST', 'DELETE'])
