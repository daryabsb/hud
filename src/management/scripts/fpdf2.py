import csv
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode
from src.products.models import Product

class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("./images/logo-02.png", 10, 8, 27, 27)
        # Setting font: helvetica bold 15
        # Moving cursor to the right:
        # self.cell(85, 37)
        # Position cursor at 1.5 cm from top:
        # Printing title:
        self.set_text_shaping(True)
        # Different styles of the same font family.
        self.add_font("AdobeArabic", style="", fname="./fonts/AdobeArabic-Bold.ttf")
        # Set and use first family in regular style.
        self.set_font(family="AdobeArabic", style="", size=24)
        self.cell(85)
        self.cell(100, 20, "كۆمپانیای لۆكس بۆ كۆنترۆڵی جۆری", border=0, align="R")
        self.ln(12)
        self.cell(85)
        self.set_font("Times", "B", 17)
        self.cell(100, 20, "Lox for Quality Control Ltd.", border=0, align="R")
        # self.add_font("AdobeArabic", style="", fname="./fonts/AdobeArabic-Bold.ttf")
        # # Set and use first family in regular style.
        # self.set_font(family="AdobeArabic", style="", size=20)
        # self.cell(55, 20, "كۆمپانیای لۆكس بۆ كۆنترۆڵی جۆری و پێدانی بڕوانامە", border=0, align="L")

        # self.cell(10, 37)
        # self.set_font("Times", "B", 14)
        # self.cell(35, 37, "Lox for Quality Control and Certification Ltd.", border=0, align="R")
        # self.set_font("helvetica", size=14)
        # Performing a line break:
        self.ln(35)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("Times", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

def run():
    pdf = PDF(format='A4')
    pdf.set_font("helvetica", size=16)
    pdf.add_page()
    pdf.cell(80)
    pdf.cell(30, -12, "Products List", border=0, align="C")
    pdf.set_font("helvetica", size=9)
    
    queryset = Product.objects.select_related(
        'parent_group', 'barcode'
        ).values_list(
            "id", "name", "parent_group__name", "barcode__value", "price"
            )
    header = [
        {"text":"ID", "align":"left", "width":10}, 
        {"text":"NAME", "align":"left", "width":25}, 
        {"text":"PARENT", "align":"left", "width":20}, 
        {"text":"BARCODE", "align":"left", "width":25},
        {"text":"PRICE", "align":"left", "width":20}]
    
    html_content = get_table_content(queryset, header)

    pdf.write_html(html_content, table_line_separators=True)
    pdf.output("html2.pdf")


def get_table_content(queryset, header):
    
    html_content = f"""
        <p></p>
        <section>
        <table width="100%">
            <thead>
                <tr>"""
    for th in header:
        html_content += f'<th bgcolor="#948b8b" align="{th["align"]}" width="{th["width"]}%"><font size=9>{th["text"]}</font></th>'
        
    html_content += f"""
    </tr>
    </thead>
    <tbody>"""
    
    for data_row in queryset:
        # data_row = model_to_dict(data_row)
        html_content += f'<tr>'
        for datum in data_row:
            html_content += f"<td><font size=9>{str(datum)}</font></td>"
        html_content += f'</tr>'
    
    html_content += """
                </tbody>
            </table>
        </section>
    """
    return html_content

'''
    # Reading CSV and creating a simple table
    with open("./countries.txt", encoding="utf8") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))

    # field_names = ['id', 'name', 'parent_group', 'barcode__code', 'price']

    # # Creating the header list based on field_names
    # header = [
    #     {"text": field.replace('_', ' ').upper(), "align": "left", "width": 20}  # Adjust width as needed
    #     for field in field_names
    # ]
    
    # pdf.set_draw_color(65, 64, 66)
    # pdf.set_line_width(0.3)
    # headings_style = FontFace(emphasis="BOLD", color=0, fill_color=(182, 182, 182))
    
    # with pdf.table(
    #     borders_layout="MINIMAL",
    #     cell_fill_color=(182, 182, 182),
    #     cell_fill_mode=TableCellFillMode.ROWS,
    #     col_widths=(15, 60, 30, 30),
    #     headings_style=headings_style,
    #     line_height=8,
    #     text_align=("LEFT", "LEFT", "LEFT", "LEFT"),
    #     width=185,
    # ) as table:
    #     # header_row = table.row()
    #     # for item in header:
    #     #     header_row.cell(item)
    #     for data_row in queryset:
    #         row = table.row()
    #         # data_row = model_to_dict(data_row)
    #         for datum in data_row:
    #             row.cell(str(datum))

    # pdf.output("template4.pdf")    

    # pdf = FPDF()
    # pdf.add_page()

    html_content ="""
    <font face="helvetica" color="#948b8b" size="28"><p align="center">Big title</p></font>
    <section>
       <font face="helvetica" color="#948b8b" size="24"><p align="center">Section title</p></font>
        <font face="helvetica" color="#948b8b" size="20"><p align="center">Product List</p><br></font>
    </section>
        
    """
'''