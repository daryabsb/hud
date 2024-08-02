# myapp/db_router.py

from src.configurations.models import ApplicationProperty as ap
ap.objects.all()


class ConfigurationsRouter:
    route_app_labels = {"src.configurations", "configurations"}
    route_model_lebels = {"ApplicationProperty",
                          "ApplicationPropertySection", "AppTable", "AppTableColumn"}
    route_modelnames = {"applicationproperty",
                        "applicationpropertysection", "apptable", "apptablecolumn"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            if model.__name__ in self.route_model_lebels:
                return 'settings_db'
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            if model.__name__ in self.route_model_lebels:
                return 'settings_db'
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            if model_name in model_name in self.route_modelnames:
                return db == 'settings_db'
            return db == 'default'
        return None
