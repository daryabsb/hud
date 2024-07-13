from django.contrib import admin
from src.printers.models import CompanyLetterhead, CompanyLetterheadOption
from src.accounts.models import User


# Register your models here.
INITIAL_DATA = [
    {"id": 1, "name": "Company Letterhead 1"},
]


@admin.register(CompanyLetterhead)
class CompanyLetterheadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'created')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, letterhead in enumerate(INITIAL_DATA):
            c_letterhead = CompanyLetterhead.objects.filter(
                id=letterhead['id']).first()
            user = User.objects.first()
            company = user.companies.first()
            if not c_letterhead:
                c_letterhead = CompanyLetterhead(**letterhead)
                c_letterhead.user = user
                c_letterhead.company = company
                if letterhead['id'] == 1:
                    c_letterhead.is_default = True
                options = CompanyLetterheadOption.objects.first()
                if not options:
                    options = CompanyLetterheadOption.objects.create(
                        user=user, name='Company Letterhead Options 1')

                c_letterhead.letterhead_options = options
                c_letterhead.save(force_insert=True)
            else:
                c_letterhead.name = letterhead['name']
                c_letterhead.save(force_update=True)


@admin.register(CompanyLetterheadOption)
class CompanyLetterheadOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'font_family', 'unicode_font', 'unicode_text_header_size', 'text_header_size',
                    'unicode_text_content_size', 'text_content_size', 'table_text_content_size')
    ordering = ('created', )
    list_filter = ('name', )
