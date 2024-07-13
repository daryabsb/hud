import csv
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode
from src.products.models import Product
from src.accounts.models import User

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


class PDF(FPDF):
    def __init__(self, user=None, queryset=None, table_header=None, *args, **kwargs):
        self.user = user or User.objects.first()
        self.company = self.user.companies.first()
        self.logo = self.user.companies.first().logo
        self.queryset = queryset
        self.table_header = table_header

    def header(self):
        self.image(self.logo.image.path, 10, 8, 27, 27)
        self.set_text_shaping(True)
        self.add_font("AdobeArabic", style="",
                      fname="./fonts/AdobeArabic-Bold.ttf")
        self.set_font(family="AdobeArabic", style="", size=24)
        self.cell(85)
        self.cell(100, 20, "كۆمپانیای لۆكس بۆ كۆنترۆڵی جۆری",
                  border=0, align="R")
        self.ln(12)
        self.cell(85)
        self.set_font("Times", "B", 17)
        self.cell(100, 20, "Lox for Quality Control Ltd.", border=0, align="R")
        self.ln(35)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_pdf(queryset):
    pass
