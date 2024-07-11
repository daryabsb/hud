from fpdf import FPDF, HTMLMixin, Template

'''
FONTS:
Courier (fixed-width)
Helvetica or Arial (synonymous; sans serif)
Times (serif)
Symbol (symbolic)
ZapfDingbats (symbolic)
'''


# this will define the ELEMENTS that will compose the template.
elements = [
    {'name': 'company_logo', 'type': 'I', 'x1': 10.0, 'y1': 10.0, 'x2': 37.0, 'y2': 37.0, 'font': None, 'size': 0.0,
        'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'logo', 'priority': 2, },


    {'name': 'company_name', 'type': 'T', 'x1': 17.0, 'y1': 32.5, 'x2': 115.0, 'y2': 37.5, 'font': 'Arial', 'size': 12.0,
        'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'C', 'text': '', 'priority': 2, },

    {'name': 'box', 'type': 'B', 'x1': 10.0, 'y1': 10.0, 'x2': 200.0, 'y2': 287.0, 'font': 'Arial', 'size': 0.0, 'bold': 0,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
    {'name': 'box_x', 'type': 'B', 'x1': 95.0, 'y1': 15.0, 'x2': 105.0, 'y2': 25.0, 'font': 'Arial', 'size': 0.0, 'bold': 1,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 2, },
    {'name': 'line1', 'type': 'L', 'x1': 100.0, 'y1': 25.0, 'x2': 100.0, 'y2': 57.0, 'font': 'Arial', 'size': 0, 'bold': 0,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
    {'name': 'barcode', 'type': 'BC', 'x1': 20.0, 'y1': 246.5, 'x2': 140.0, 'y2': 254.0, 'font': 'Interleaved 2of5 NT', 'size': 0.75, 'bold': 0,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'C', 'text': '200000000001000159053338016581200810081', 'priority': 3, },
]

title = '20000 Leagues Under the Seas'


class PDF(FPDF):
    def header(self):
        # Logo
        self.image("./images/logo-02.png", 10, 10, 27)
        # Arial bold 15
        self.set_font('Arial', 'B', 9.21)

        self.set_y(37)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, -15, 'Tic Company', 0, 0, 'C')
        # Line break
        self.ln(5)

    # # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)


def run():
    # USING FPDF Class

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    for i in range(1, 25):
        pdf.cell(0, 8, 'Printing line ' + str(i), 0, 1)
    pdf.output('template2.pdf', 'F')


html = """
<H1 align="center">html2fpdf</H1>
<h2>Basic usage</h2>
<p>You can now easily print text mixing different
styles : <B>bold</B>, <I>italic</I>, <U>underlined</U>, or
<B><I><U>all at once</U></I></B>!<BR>You can also insert links
on text, such as <A HREF="http://www.fpdf.org">www.fpdf.org</A>,
or on an image: click on the logo.<br>
<center>
<A HREF="http://www.fpdf.org"><img src="tutorial/logo.png" width="104" height="71"></A>
</center>
<h3>Sample List</h3>
<ul><li>option 1</li>
<ol><li>option 2</li></ol>
<li>option 3</li></ul>

<table border="0" align="center" width="50%">
<thead><tr><th width="30%">Header 1</th><th width="70%">header 2</th></tr></thead>
<tbody>
<tr><td>cell 1</td><td>cell 2</td></tr>
<tr><td>cell 2</td><td>cell 3</td></tr>
</tbody>
</table>
"""
'''
    def header(self):
        # Arial bold 15
        self.add_font('AdobeArabic', '',
                      r'./fonts/AdobeArabic-Bold.ttf', uni=True)
        self.set_font('Times', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)



    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    # USING TEMPLATE
    # here we instantiate the template and define the HEADER
    f = Template(format="A4", elements=elements,
                 title="Sample Invoice")
    f.add_page()
    # we FILL some of the fields of the template with the information we want
    # note we access the elements treating the template instance as a "dict"
    f["company_name"] = "Tic Company"
    f["company_logo"] = "./images/logo-02.png"
    # and now we render the page
    f.render("./template.pdf")


    # pdf = PDF()
    # pdf.set_title(title)
    # pdf.set_author('Jules Verne')
    # pdf.print_chapter(1, 'A RUNAWAY REEF', '20k_c1.txt')
    # pdf.print_chapter(2, 'THE PROS AND CONS', '20k_c2.txt')
    # pdf.output('template3.pdf', 'F')
    pdf = MyFPDF()
    # First page
    pdf.add_page()
    pdf.write_html(html)
    pdf.output('template4.pdf', 'F')

'''
