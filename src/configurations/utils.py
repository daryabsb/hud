from src.configurations.models import ApplicationProperty


def get_application_property(name):
    return ApplicationProperty.objects.get(name=name)
