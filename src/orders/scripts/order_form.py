from src.orders.forms import DocumentForm
from src.accounts.models import User
from src.documents.models import DocumentType


# print(form['number'].value())

# print(form['customer'].value())
# None
# form.save()

# document = form.save(commit=False)
# document.user = user
# document.save()


# document.document_type = dt
# document.save()

[
    'Meta', 'add_error', 'add_initial_prefix', 'add_prefix', 'as_div', 'as_p',
    'as_table', 'as_ul', 'base_fields', 'changed_data', 'clean', 'declared_fields',
    'default_renderer', 'errors', 'field_order', 'full_clean', 'get_context',
    'get_initial_for_field', 'has_changed', 'has_error', 'hidden_fields', 'is_multipart',
    'is_valid', 'media', 'non_field_errors', 'order_fields', 'prefix', 'render', 'save',
    'template_name', 'template_name_div', 'template_name_label', 'template_name_p',
    'template_name_table', 'template_name_ul', 'use_required_attribute', 'validate_unique',
    'visible_fields'
]


def run(*args):
    dt = int(args[0])
    document_type = DocumentType.objects.get(id=dt)
    user = User.objects.first()

    form = DocumentForm(initial={'document_type': document_type, 'user': user})

    print('Script is smooooth = ', int(args[0]))
