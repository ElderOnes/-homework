import inspect


def introspection_info(obj):
    obj_type = type(obj).__name__

    attributes = [attr for attr in dir(obj) if not attr.startswith('__')]

    methods = [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith('__')]

    module = getattr(obj, '__module__', None)

    additional_info = {}
    if isinstance(obj, (list, dict, set, str)):
        additional_info['length'] = len(obj)

    info = {
        'type': obj_type,
        'attributes': attributes,
        'methods': methods,
        'module': module,
        **additional_info,
    }

    return info


class SampleClass:
    def __init__(self):
        self.attribute1 = "value1"
        self.attribute2 = "value2"

    def method1(self):
        return "This is method1"


sample_object = SampleClass()

sample_info = introspection_info(sample_object)
print(sample_info)

number_info = introspection_info(42)
print(number_info)
