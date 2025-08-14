from src.documents.models import DocumentType
from django.forms import model_to_dict


def run():
    queryset = DocumentType.objects.all()
    dt_list = []
    for document_type in queryset:
        dt_list.append(model_to_dict(document_type))
    print(dt_list)
    return dt_list
