from django.utils.translation import gettext_lazy as _

USER_PLAN_CACHE_PREFIX = 'user_plans'
ACTIVATION_CODE_PREFIX = 'activation_code'
SUBSCRIPTION_PREFIX = 'subscriptions'
COMPANY_PREFIX = 'companies'
STORE_PREFIX = 'stores'

UNREAD, READ = (0, 1)

NOTICE_STATUS = (
    (
        UNREAD, _('userNotification.statusOpts.unread')),
    (
        READ, _('userNotification.statusOpts.read')))

USERPLAN_EXPIRED = 101

EVENTS = (
    (
        USERPLAN_EXPIRED, _('userPlan.events.expired')),
)

CATEGORY_COMPANY = 100
CATEGORY_STORE = 101
CATEGORY_USERPLAN = 102
CATEGORY_ACTIVATION_CODE = 103
CATEGORY_SUBSCRIPTION = 104
CATEGORY_PLAN = 105
CATEGORY_DOCUMENT = 106
CATEGORY_SECURITY = 107

USER_NOTIFICATION_CATEGORIES = (
    (CATEGORY_COMPANY, 'Company'),
    (CATEGORY_STORE, 'Store'),
    (CATEGORY_USERPLAN, 'User_Plan'),
    (CATEGORY_ACTIVATION_CODE, 'Activation_Code'),
    (CATEGORY_SUBSCRIPTION, 'Subscription'),
    (CATEGORY_PLAN, 'Plan'),
    (CATEGORY_DOCUMENT, 'Document'),
    (CATEGORY_SECURITY, 'Security'),
)

CATEGORIES_DICT = dict((x, y) for x, y in USER_NOTIFICATION_CATEGORIES)

(
    CO_COMPANY,
    ST_STORE,
    UP_USERPLAN,
    AC_ACTIVATION_CODE,
    SB_SUBSCRIPTION,
    PP_PLAN,
    DC_DOCUMENT,
    SEC_SECURITY
) = (1, 2, 3, 4, 5, 6, 7, 8)

(
    LATE_IN,
    EARLY_OUT,
    ABSENCE,
    PENDING,
    APPROVED,
    REJECTED,
    ATT_ALL,
    MTD,
    NORMAL_SCHEDULE,
    TEMPORARY_SCHEDULE,
) = (1, 2, 3, 4, 5, 6, 7, 201, 202, 203)

'''
main: model_name
with user: model_name ::: user.id
with obj: model_name ::: user.id ::: number
with obj and without user: model_name ::: number
'''


def get_prefix(prefix, user=None, number=None):
    if user and not user.is_superuser:
        return prefix + ':::' + str(user.id)
    if user and not user.is_superuser:
        return prefix + ':::' + str(user.id)
    return prefix


def delete_cache(prefix, user=None, number=None):
    """
    Delete cache for the specified model and its variations based on user and number.

    :param model_name: The name of the model.
    :param user: The user for whom the cache should be deleted (if applicable).
    :param number: The specific object number (if applicable).
    """
    from django.core.cache import cache

    # Cache key for all objects of the model
    cache_key_all = f"{prefix}"

    # Cache key for all objects for a particular user
    if user is not None:
        user_id = str(user.id)
        cache_key_user = f"{prefix}:::{user_id}"

    # Cache key for an individual object without a user
    if number is not None:
        cache_key_individual = f"{prefix}:::{number}"

    # Cache key for an individual object with a user
    if user is not None and number is not None:
        user_id = str(user.id)
        cache_key_individual_user = f"{prefix}:::{user_id}:::{number}"

    # Delete the cache for all the specified cases
    cache.delete(cache_key_all)
    if user is not None:
        cache.delete(cache_key_user)
    if number is not None:
        cache.delete(cache_key_individual)
    if user is not None and number is not None:
        cache.delete(cache_key_individual_user)
