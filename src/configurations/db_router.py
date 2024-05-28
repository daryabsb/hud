# myapp/db_router.py

class ApplicationSettingsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'configurations' and model.__name__ == 'ApplicationProperty':
            return 'settings_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'configurations' and model.__name__ == 'ApplicationProperty':
            return 'settings_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label == 'configurations' and obj1.__class__.__name__ == 'ApplicationProperty') or \
           (obj2._meta.app_label == 'configurations' and obj2.__class__.__name__ == 'ApplicationProperty'):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'configurations' and model_name == 'applicationproperty':
            return db == 'settings_db'
        return None
