from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import override
from django.db.models import signals, ForeignKey
from django.db import connections, router
from src._utils import cprint

DJANGO_NATIVE_PERMISSION = {
    'add', 'change', 'delete'}
PERM_FIRST_TIME_SET = None


def check_and_create_model_initial_data(model):
    """
    check initial_data existent, if it is vacant, then create it
    :param model:
    :return:
    """
    if not (hasattr(model, 'Admin') and hasattr(model.Admin, 'initial_data')):
        return
    datum = getattr(model.Admin, 'initial_data')
    if isinstance(datum, (list, tuple)):
        pass
    else:
        if callable(datum):
            model.Admin().initial_data()


def remove_permission(**kwargs):
    """
    :param kwargs:  query kwargs
    :return:
    """
    import json
    try:
        obsolete_perm = Permission.objects.get(**kwargs)
    except Permission.DoesNotExist:
        pass
    else:
        cprint('[REMOVE] {} within {}'.format(kwargs.get('codename'),
               json.dumps(obsolete_perm.content_type.natural_key())), 'red')
        obsolete_perm.delete()


def insert_permission(**kwargs):
    """
    :param kwargs:
    :return:
      * 1 -- inserted
      * 0 -- existed
      * -1 -- error
    """
    from django.db import ProgrammingError
    from django.db import DatabaseError
    try:
        Permission.objects.get(**kwargs)
    except Permission.DoesNotExist:
        try:
            (Permission.objects.create)(**kwargs)
            maintain_perms_cache(op='update')
        except (ProgrammingError, DatabaseError) as e:
            try:
                cprint('! Failed to insert permission {}: {}'.format(
                    kwargs.get('codename'), e), 'red')
                return -1
            finally:
                e = None
                del e

        else:
            cprint(
                '+ Successful to insert permission {}'.format(kwargs.get('codename')), 'green')
            return 1

    else:
        return 0


def _insert_view_permission(ct, model_name):
    code_name = 'view_' + model_name
    human_name = 'Can view {}'.format(model_name)
    insert_permission(content_type=ct, codename=code_name, name=human_name)


def _remove_obsolete_browse_permission(ct, model_name):
    code_name = 'browse_' + model_name
    remove_permission(content_type=ct, codename=code_name)


def admin_initial_data(admin):
    """
    parse initial_data from src.admin class
    :param admin:
    :return:
    """
    initial_data = admin.initial_data
    if callable(initial_data):
        try:
            initial_data()
        except Exception:
            import traceback
            traceback.print_exc()

    else:
        if isinstance(initial_data, (list, tuple)):
            pass


def maintain_model_initial_data(**kwargs):
    from src.accounts.models import Company, Store, Logo

    app_config = kwargs.get('app_config')
    db = kwargs.get('using')
    connection = connections[db]
    user_model = get_user_model()
    if user_model.objects.count() == 0:
        super_user = user_model.objects.create_superuser(
            'root@root.com', 'root')
        super_user.name = 'Super Admin'
        super_user.save()
    admin_user = user_model.objects.get(id=1)

    admin_user_company = Company.objects.filter(
        user=admin_user).first()

    admin_user_store = Store.objects.filter(
        user=admin_user).first()

    default_logo = Logo.objects.first()
    if not default_logo:
        default_logo = Logo.objects.create()

    if not admin_user_company and not admin_user_store:
        admin_company = Company.objects.create(
            user=admin_user,
            name='Default_Admin_Company',
            logo=default_logo,
            is_default=True
        )
        Store.objects.create(
            user=admin_user,
            company=admin_company,
            name='Default_Admin_Store',
            logo=default_logo,
            is_default=True
        )

    for model in router.get_migratable_models(app_config,
                                              (connection.alias), include_auto_created=False):

        content_type = ContentType.objects.get_for_model(
            model, for_concrete_model=False)
        _app_label, model_name = content_type.natural_key()
        # _remove_obsolete_browse_permission(
        #     content_type, model_name)
        # default_permissions = model._meta.default_permissions
        # if model_name == 'group':
        #     default_permissions = ('add', 'change', 'view')
        # if default_permissions:
        #     extraneous_permission = DJANGO_NATIVE_PERMISSION - \
        #         set(default_permissions)
        #     _insert_view_permission(content_type, model_name)
        # else:
        #     if model._meta.proxy:
        #         _insert_view_permission(content_type, model_name)
        #         extraneous_permission = []
        #     else:
        #         extraneous_permission = DJANGO_NATIVE_PERMISSION | {
        #             'view'}
        # for perm_prefix in extraneous_permission:
        #     code_name = '{}_{}'.format(perm_prefix, model_name)
        #     remove_permission(
        #         content_type=content_type, codename=code_name)

        check_and_create_model_initial_data(model)
        admin_site = admin.site
        if model in admin_site._registry:
            admin_class = admin_site._registry[model]
            if hasattr(admin_class, 'initial_data'):
                admin_initial_data(admin_class)
            else:
                handle_action_permission(
                    admin_class, content_type, model_name)


def handle_action_permission(admin_class, content_type, model_name, **kwargs):
    from src.core.utils import hungary_notation, get_args_form_dict
    from src.core.utils import remove_duplicate_elements
    only_class = get_args_form_dict('only_class', kwargs, bool, False)
    need_return = get_args_form_dict('need_return', kwargs, bool, False)
    insert_perms = get_args_form_dict('insert_perms', kwargs, bool, True)
    actions = []
    for klass in admin_class.__class__.mro()[:2][::-1]:
        for attr_key in ('actions', 'action_sets'):
            if attr_key not in klass.__dict__:
                continue
            else:
                class_actions = getattr(klass, attr_key, None)
            if class_actions is None:
                continue
            if attr_key == 'actions':
                if only_class and not insert_perms:
                    actions.extend(class_actions)
                else:
                    actions.extend([admin_class.get_action(action)
                                   for action in class_actions])
            else:
                class_action_sets = class_actions
                for action_set in class_action_sets:
                    if only_class:
                        if not insert_perms:
                            actions.append((action_set.name, action_set.cls))
                        actions.extend([admin_class.get_action(action)
                                       for action in action_set.cls])

    actions = [_f for _f in actions if _f]
    actions = remove_duplicate_elements(actions)
    if insert_perms:
        seen = set()
        for _klass, name, desc in actions:
            code_name = '{0}_{1}'.format(hungary_notation(name), model_name)
            if name in ('GeneralActionDelete', 'GeneralActionNew'):
                remove_permission(content_type=content_type,
                                  codename=code_name)
                continue
            if name not in seen:
                with override('en'):
                    human_name = 'Can {verb} {target}'.format(
                        verb=name, target=model_name)
                    ret = insert_permission(
                        content_type=content_type, name=human_name, codename=code_name)
                    if ret >= 0:
                        seen.add(name)

    if need_return:
        return actions
    return


def maintain_perms_cache(**kwargs):
    """
    maintain perms cache in cache backend
    :param kwargs:
    :return:
    """
    from django.db.models import Value as V, CharField
    from django.db.models.functions import Concat
    CACHE_KEY_PERM = 'current_existent_perm'

    op = kwargs.get('op', '')
    _cache = cache.get(CACHE_KEY_PERM)
    _valid = _cache is not None
    if op == 'check':
        return _valid
    if op == 'fetch':
        return _cache
    if op in ('update', 'set'):
        if op == 'update':
            if _cache is not None:
                cache.delete(CACHE_KEY_PERM)
        if op == 'set':
            if _valid:
                return False
        current_existent_perms = Permission.objects.annotate(
            the_custom_key=Concat(
                'content_type__app_label',
                (V('.')),
                'codename',
                output_field=(CharField()))).values_list('the_custom_key', flat=True)
        cache.set(CACHE_KEY_PERM, frozenset(
            current_existent_perms), 86400)
        return frozenset(current_existent_perms)


def post_syncdb_initial_data(**kwargs):
    global PERM_FIRST_TIME_SET
    # from django_redis import get_redis_connection
    maintain_model_initial_data(**kwargs)
    # get rid of all caches
    # get_redis_connection('default').flushall()
    if PERM_FIRST_TIME_SET is None:
        cprint('update permissions. (it shall run merely one time.)', 'green')
        # process_extra_permission()
        maintain_perms_cache(op='update')
        # maintain_action_cache(force_update=True)
        PERM_FIRST_TIME_SET = False


signals.post_migrate.connect(post_syncdb_initial_data)
