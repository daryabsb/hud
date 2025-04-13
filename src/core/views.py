from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from src.core.utils import get_fields, get_columns, get_searchable_fields
from django.http import JsonResponse

# Create your views here.


def index(request):
    return render(request, 'index.html')


def not_authorized(request):
    return render(request, 'not-authorized.html')


def search_datatable(request, app_name=None, model=None):
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
