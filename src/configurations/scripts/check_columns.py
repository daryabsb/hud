from src.core.utils import get_fields, get_columns
from src.documents.models import DocumentItem


def run():
    fields = [field for field in DocumentItem._meta.get_fields()]
    documents_row = [field.name for field in fields if not (
        field.many_to_many or field.one_to_many)]

    print(documents_row)

    # print(get_fields('products'))
    # print(get_columns('products'))
