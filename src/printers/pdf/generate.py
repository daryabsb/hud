import csv
from src.printers.pdf.fpdf import PDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode
from src.products.models import Product
from src.accounts.models import User, Company


kwargs = {
    "logo": "./images/logo-02.png",
    "company_name_ar": "كۆمپانیای لۆكس بۆ كۆنترۆڵی جۆری",
    "company_name_en": "Lox for Quality Control Ltd.",
    "document_title": "Product List",
}
options = {
    "font_family": "helvetica",
    "unicode_font_family": "AdobeArabic",
    "unicode_font_location": "AdobeArabic",
    "en_header_text_size": 17,
    "ar_header_text_size": 24,
}





def generate_pdf(queryset, user=None):
    if not user:
        user = User.objects.first()

    active_company = user.companies.filter(is_default=True).first()
    pdf = PDF(company=active_company)
    
    print(pdf.company.name)
