from src.management.utils import generate_pdf, generate_invoice


def run():
    generate_invoice()


context = {
    'RML_DIR': 'C:\\api\\hud\\src\\_utils\\rml',
    'fund': '<Fund: New Movie>',
    'live_themes': '<QuerySet [<Theme: General - New Movie>]>',
    'line_chart_data': [
        [('20240712', 100.0)], [('20240712', 100.0)]

    ],
    'attribution': {
        'data': [['General'], [2e-07]],
        'lookup': [['Kurdistan'], ['Tangible']],
        'Kurdistan': {
            'Tangible': 2e-07,
            'total': 2e-07},
        'Tangible': 2e-07
    }
}
