
class DjangoCustomModel:
    def __init__(self, data):
        self.data = data

    def filter(self, **kwargs):
        filtered_list = []

        def matches_nested_attrs(item, nested_attrs):
            for key, value in nested_attrs.items():
                if '__' in key:
                    # Handle nested attributes using double underscores
                    keys = key.split('__')
                    current_item = item
                    for k in keys:
                        if isinstance(current_item, dict) and k in current_item:
                            current_item = current_item[k]
                        else:
                            return False
                    if current_item != value:
                        return False
                elif key not in item or item[key] != value:
                    return False
            return True

        for item in self.data:
            if matches_nested_attrs(item, kwargs):
                filtered_list.append(item)

        return DjangoCustomModel(filtered_list)

    def count(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

def filter_list(objects, **kwargs):
    filtered_list = []
    for obj in objects:
        match = True
        for key, value in kwargs.items():
            if not hasattr(obj, key) or getattr(obj, key) != value:
                match = False
                break
        if match:
            filtered_list.append(obj)
    return filtered_list