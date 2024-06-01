from src.configurations.models import ApplicationProperty
from loguru import logger
from collections import defaultdict

# Assuming we have the ApplicationProperty objects already fetched from the database


def nested_settings(properties):
    settings_dict = defaultdict(lambda: {"name": "", "rows": []})

    for prop in properties:
        levels = prop.name.split('.')

        for i, level in enumerate(levels):
            current_level = {}
            if i == len(levels) - 1:
                # This is the last level, which contains the value
                current_level[level] = {"name": level, "value": {
                    "id": prop.id, "name": prop.name, "value": prop.value}}
            else:
                if level not in current_level:
                    current_level[level] = {"name": level, "rows": []}
                current_level = current_level[level]["rows"]

    def dict_to_list(d):
        result = []
        for key, value in d.items():
            if isinstance(value, dict) and "rows" in value:
                value["rows"] = dict_to_list(value["rows"])
            result.append(value)
        return result

    # Convert the nested dictionary to a list format
    return dict_to_list(settings_dict)


def run():
    properties = ApplicationProperty.objects.all()
    # Convert the properties to the nested settings list
    logger.success(f"Testing properties:> {properties.first().name}")

    nested_settings_list = nested_settings(properties)

    logger.success("Testing started:>")
    print(nested_settings_list)
    logger.success("Testing finished:>")
