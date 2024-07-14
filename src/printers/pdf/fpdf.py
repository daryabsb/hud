from fpdf import FPDF


class MyPDF(FPDF):
    def __init__(self, user=None, queryset=None, table_name='Invoice', table_header=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.queryset = queryset
        self.table_header = table_header
        self.table_name = table_name
        
        self.company = self.user.companies.filter(is_default=True).first()
        if not self.company:
            raise ValueError("Default company not found for the user.")
        
        self.logo = self.company.logo
        self.options = self.get_options()
        self.main_font_family = self.options.font_family
        self.unicode_text_header_size = self.options.unicode_text_header_size
        self.text_header_size = self.options.text_header_size

        self.logo_path = self.logo.image.path

        self.unicode_font_family, self.unicode_font_path = self.get_font_family()
        self.company_ar_name = self.company.ar_name
        self.company_name = self.company.name

        self.generate_pdf()

    def get_letterhead(self):
        letterhead = self.company.letterheads.filter(is_default=True).first()
        if not letterhead:
            raise ValueError("Default letterhead not found for the company.")
        return letterhead
    
    def get_options(self):
        letterhead = self.get_letterhead()
        if not letterhead.letterhead_options:
            raise ValueError("Letterhead options not found.")
        return letterhead.letterhead_options
        
    def get_font_family(self):
        from fontTools.ttLib import TTFont
        unicode_font_path = self.get_options().unicode_font.path
        font = TTFont(unicode_font_path)
        name_records = font['name'].names
        for record in name_records:
            if record.nameID == 1:  # Font Family name
                return record.toUnicode(), unicode_font_path
        raise ValueError("Font family name not found in the font file.")
    
    def get_paper_measures(self):
        if self.cur_orientation == "P":
            return self.options.inner_width, self.options.inner_height
        else:
            return self.options.inner_height, self.options.inner_width


    def header(self):
        width, height = self.get_paper_measures()

        self.image(self.logo_path, 10, 8, 65, 19)
        self.set_text_shaping(True)
        self.add_font(self.unicode_font_family, style="", fname=self.unicode_font_path)
        self.set_font(family=self.unicode_font_family, style="", size=self.unicode_text_header_size)

        self.cell(2/5 * width)
        self.cell(3/5 *width , 15, self.company_ar_name, border=0, align="R")
        self.ln(12)
        self.cell(2/5 * width)
        self.set_font(self.main_font_family, "B", self.text_header_size)
        self.cell(3/5 *width, 15, self.company_name, border=0, align="R")
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.main_font_family, "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def generate_pdf(self):
        self.set_margins(
            left=self.options.left_margin,
            top=self.options.top_margin,
            right=self.options.right_margin,
            )
        width, height = self.get_paper_measures()

        self.set_font("helvetica", size=16)
        self.add_page()
        # self.cell(80)

        self.cell(width, -12, self.table_name, border=0, align="C")
        self.set_font(self.font_family, size=9)

        html_content = self.get_table_content(self.queryset, self.table_header)
        self.write_html(html_content, table_line_separators=True)
    
    def add_unicode_company_name(self):
        if self.cur_orientation == 'P':
            self.cell(85)
            self.cell(100, 20, self.company_ar_name, border=0, align="R")
        else:
            self.cell(85)
            self.cell(100, 20, self.company_ar_name, border=0, align="R")

    
    def get_table_content(self, queryset, header):
        html_content = """
        <p></p>
        <section>
        <table width="100%">
            <thead>
                <tr>"""
        for th in header:
            html_content += f'<th bgcolor="#948b8b" align="{th["align"]}" width="{th["width"]}%"><font size=9>{th["text"]}</font></th>'

        html_content += """
                </tr>
            </thead>
            <tbody>"""

        for data_row in queryset:
            html_content += '<tr>'
            for datum in data_row:
                html_content += f"<td><font size=9>{str(datum)}</font></td>"
            html_content += '</tr>'

        html_content += """
            </tbody>
        </table>
        </section>
        """
        return html_content