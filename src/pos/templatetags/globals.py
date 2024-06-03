from django import template
from django.urls import resolve
from django.urls.exceptions import Resolver404
from loguru import logger


register = template.Library()

# This the custom filter, name is getitems


def getdata(json_data, args):
    func_name = ''
    try:
        myfunc, myargs, mykwargs = resolve(args)
        if myfunc:
            logger.success("*"*50)
            print()
            logger.debug("Function Name:> {} ",
                         myfunc.__name__, feature="f-strings")
            logger.debug("Module Name:> {} ",
                         myfunc.__module__, feature="f-strings")
            logger.debug("URL_Path:> {} ", args, feature="f-strings")
            func_name = myfunc.__name__
            print()
            logger.success("*"*50)
    except Resolver404:
        logger.debug("something went wrong", feature="f-strings")
        pass

    # return json_data.get(func_name)
    return json_data.get(func_name)


register.filter('getdata', getdata)


def split(val, args):
    return val.split(args)

register.filter('split', split)


def load(str, args=None):
    import json, ast
    try:
        # Parse the JSON string into a Python list
        result_list = json.loads(str)
        # Convert 'true'/'false' strings to boolean True/False
        for item in result_list:
            if item['show'] == 'true':
                item['show'] = True
            elif item['show'] == 'false':
                item['show'] = False

        print("result_list = ", result_list)
        # print("type = ", type(result_list))

        return result_list
    except json.JSONDecodeError as e:
        # Handle the error if the string is not a valid JSON
        print(f"Error decoding JSON: {e}")
        return None

    # print("Str is: ", s)
    # print("Type Str is: ", type(s))

    # return s

register.filter('load', load)

def multiply(val1, val2):
    return val1*val2


register.filter('multiply', multiply)
