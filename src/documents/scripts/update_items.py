import random
from datetime import date
from src.documents.models import DocumentItem
from src.core.utils import generate_number
from src.accounts.models import User
user = User.objects.first()


def run():
    document_items = DocumentItem.objects.all()
    pre_num = None
    for item in document_items:
        # number = generate_number('item')
        # print('generated_number = ', number)
        # min = 100
        # max = 3999
        # digits = str(random.randint(min, max))
        # digits = (len(str(max))-len(digits))*'0'+digits
        # target = 'item'
        # print(digits)

        # item.number = f'{target}-{user.id}-{item.created.strftime("%d%m%Y")}-01-{digits}'
        # item.number = number
        # item.save()
        new_num = item.number
        if new_num == pre_num:
            print(item.number)
        else:
            pre_num = item.number
