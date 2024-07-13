from .filters import filter_list, DjangoCustomModel
from .termcolor import cprint, colored


def get_font_family(font_path):
    from fontTools.ttLib import TTFont
    font = TTFont(font_path)
    name_records = font['name'].names
    for record in name_records:
        if record.nameID == 1:  # Font Family name
            return record.toUnicode()
