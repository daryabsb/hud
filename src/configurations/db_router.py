# myapp/db_router.py

class ConfigurationsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'src.configurations':
            if model.__name__ == 'ApplicationProperty':
                return 'settings_db'
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'src.configurations':
            if model.__name__ == 'ApplicationProperty':
                return 'settings_db'
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'src.configurations' and obj2._meta.app_label == 'src.configurations':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'src.configurations':
            if model_name == 'ApplicationProperty' or model_name == 'applicationproperty':
                return db == 'settings_db'
            return db == 'default'
        return None
