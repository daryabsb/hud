from django import template


register = template.Library()


def split(val, args):
    return val.split(args)


# register.filter('split', split)
