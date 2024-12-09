import random
import string
from django.contrib.auth.models import Group as UserGroup, Permission
from pytz import timezone
from src.accounts.models import User
from django.contrib.contenttypes.models import ContentType
from src.management.const import list_permissions_template, add_actions_to_models
from copy import deepcopy

from reportlab.lib import colors
from reportlab.graphics.shapes import (Drawing, Rect, String, Line, Group)
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

import os
import io
from src.settings.components import PROJECT_PATH
from reportlab.pdfgen import canvas
import preppy
from src.accounts.models import Region
from src.finances.models import (
    Fund, FundValue, IndexValue, AssetClass,
    Theme
)

WRITE_RML = True
RML_DIR = os.path.join(PROJECT_PATH, '_utils', 'rml')


def get_line_chart_data(id):
    # We have some fake time series values in the database.
    # Grab these and normalise so that start at 100

    fund = Fund.objects.get(pk=id)
    fundData = FundValue.objects.filter(fund=fund).order_by('date')
    indexData = IndexValue.objects.all().order_by('date')
    data1 = []
    data2 = []
    categoryNames = []
    data_scale = fundData[0].value / 100.0
    index_scale = indexData[0].value / 100.0
    for x in range(len(fundData)):
        data1.append((fundData[x].date.strftime(
            '%Y%m%d'), (fundData[x].value / data_scale)))
        data2.append((indexData[x].date.strftime(
            '%Y%m%d'), (indexData[x].value / index_scale)))
    return [data1, data2]


def get_attribution_data(id):
    # more fake data to drive one of the charts.
    AUMSCALE = 10000000.0
    fund = Fund.objects.get(pk=id)
    context = {}
    context['data'] = [[], []]
    context['lookup'] = [[], []]
    for r in Region.objects.all():
        context[r.name] = {}
        for ac in AssetClass.objects.all():
            context[r.name][ac.name] = 0
            context[ac.name] = 0
        context[r.name]['total'] = 0
        context['lookup'][0].append(r.name)
    for ac in AssetClass.objects.all():
        context['lookup'][1].append(ac.name)
    for ft in Theme.objects.filter(fund=fund).order_by("position__LTD"):
        context['data'][0].append(ft.name)
        context['data'][1].append(ft.position.LTD/AUMSCALE)
        context[ft.region.name][ft.asset_class.name] += ft.position.LTD / AUMSCALE
        context[ft.region.name]['total'] += ft.position.LTD / AUMSCALE
        context[ft.asset_class.name] += ft.position.LTD / AUMSCALE
    return context


def generate_invoice(id=1):
    template_file = preppy.getModule(os.path.join(RML_DIR, 'fundreport.prep'))
    fund = Fund.objects.get(pk=id)
    # fund = Fund.objects.first()

    context = {}
    context['RML_DIR'] = RML_DIR

    context['fund'] = fund
    context['live_themes'] = fund.themes.filter(live=True)

    context['line_chart_data'] = get_line_chart_data(fund.pk)
    context['attribution'] = get_attribution_data(fund.pk)
    print(context)
    rml = template_file.getOutput(context)

    if WRITE_RML:
        open(os.path.join(RML_DIR, 'latest.rml'), 'w').write(rml)
    buf = io.BytesIO()  # io.StringIO()

    # The magic step, converting the RML to PDF
    p = canvas.Canvas(buf)

    # Return the PDF for the view to return to the user
    print('We are good to go: ', buf.getvalue())

    return p


def generate_barcode():
    # Generate a 12-digit numeric barcode
    return ''.join(random.choices(string.digits, k=12))


def populate_users_permissions(users=None):
    list_permissions = add_actions_to_models(list_permissions_template)
    if not users:
        users = User.objects.all()

    users_permissions = [{'user': user, 'list_permissions': deepcopy(
        list_permissions)} for user in users]

    for user_perm in users_permissions:
        list_permissions = user_perm['list_permissions']

        for app_data in list_permissions:
            app_label = app_data['app_label']
            models_data = app_data['models']

            for model_data in models_data:
                model_name = model_data['model']

                # Retrieve ContentType for the model
                try:
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model_name)

                    # Retrieve permissions associated with this ContentType for the user
                    permissions = Permission.objects.filter(
                        content_type=content_type, user=user_perm['user'])

                    # Update actions with actual permission values
                    model_actions = model_data['actions']

                    for action in model_actions:
                        # Convert action name to lowercase (e.g., 'add')
                        action_name = action['name'].lower()
                        action['state'] = any(
                            perm.codename == f'{action_name}_{model_name}' for perm in permissions)

                except ContentType.DoesNotExist:
                    # Handle case where ContentType does not exist (should not normally happen)
                    pass

    return users_permissions


def populate_groups_permissions(groups=None):
    list_permissions = add_actions_to_models(list_permissions_template)

    if not groups:
        groups = UserGroup.objects.all()

    groups_count = groups.count

    groups_permissions = [{'group': group, 'list_permissions': deepcopy(
        list_permissions)} for group in groups]

    for group_perm in groups_permissions:
        list_permissions = group_perm['list_permissions']

        for app_data in list_permissions:
            app_label = app_data['app_label']
            models_data = app_data['models']

            for model_data in models_data:
                model_name = model_data['model']

                # Retrieve ContentType for the model
                try:
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model_name)

                    # Retrieve permissions associated with this ContentType for the group
                    permissions = Permission.objects.filter(
                        content_type=content_type, group=group_perm['group'])

                    # Update actions with actual permission values
                    model_actions = model_data['actions']

                    for action in model_actions:
                        # Convert action name to lowercase (e.g., 'add')
                        action_name = action['name'].lower()
                        action['state'] = any(
                            perm.codename == f'{action_name}_{model_name}' for perm in permissions)

                except ContentType.DoesNotExist:
                    # Handle case where ContentType does not exist (should not normally happen)
                    pass
    # groups_permissions['count'] = groups_count

    return groups_permissions


def generate_pdf():
    # font
    registerFont(TTFont("Times", "./Times.ttf"))

    drawing = Drawing(400, 200)
    # beige rectangle
    r1 = Rect(0, 0, 400, 200, 0, 0)
    r1.fillColor = colors.beige
    drawing.add(r1)

    # logo
    wave = Group(
        Line(10, -5, 10, 10),
        Line(20, -15, 20, 20),
        Line(30, -5, 30, 10),
        Line(40, -15, 40, 20),
        Line(50, -5, 50, 10),
        Line(60, -15, 60, 20),
        Line(70, -5, 70, 10),
        Line(80, -15, 80, 20),
        Line(90, -5, 90, 10),
        String(25, -25, "Wave Audio", fontName='Times')
    )
    wave.translate(10, 170)
    drawing.add(wave)

    # name
    name = Group(
        String(
            0,
            100,
            "Jane Doe",
            textAnchor='middle',
            fontName='Times',
            fontSize=18,
            fillColor=colors.black
        ),
        Line(
            -50,
            85,
            50,
            85,
            strokeColor=colors.grey,
            strokeLineCap=1,
            strokeWidth=2
        ),
        String(
            0,
            60,
            "Audio Specalist",
            textAnchor='middle',
            fontName='Times',
            fontSize=15,
            fillColor=colors.black
        )
    )
    name.translate(290, 10)
    drawing.add(name)

    # contact info
    info = Group(
        String(
            0,
            30,
            "T: +447777777777",
            fontName='Times',
            fontSize=10,
            fillColor=colors.black
        ),
        String(
            0,
            20,
            "E: jane@audio.com",
            fontName='Times',
            fontSize=10,
            fillColor=colors.black
        ),
        String(
            0,
            10,
            "www.waveaudio.com",
            fontName='Times',
            fontSize=10,
            fillColor=colors.black
        )
    )
    info.translate(20, 10)
    drawing.add(info)

    # save
    drawing.save(formats=['pdf', 'png'], outDir=".", fnRoot="card")


index_dict = {
    'product': '0',
    'customer': '3',
    'document_type': '5',
}


def apply_document_filters(request, qs):
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


def apply_column_filters(request, qs, columns, fields):
    for index, column in enumerate(columns):
        col_search_value = request.GET.get(
            f"columns[{index + 1}][search][value]", None)
        col_search_data = column['data']

        # Debug: Print the values to check what's being used
        print(f"Column Index: {index}")
        print(f"Column Data: {col_search_data}")
        print(f"Search Value: {col_search_value}")

        if col_search_value and col_search_data in fields:

            filter_key = col_search_data
            filter_dict = {filter_key: col_search_value}
            # print(f"Applying Filter: {filter_key} = {col_search_value}")
            if col_search_value == 'false':
                col_search_value = False
            else:
                col_search_value = True

            qs = qs.filter(
                # **filter_dict
                # Q(customer=customer)
                Q(document_type__id=int(col_search_value))
                # | Q(id=col_search_value)
                # | Q(paid_status=bool(col_search_value))
            )
            # print(f"QuerySet after filter: {qs.query}")

    return qs
