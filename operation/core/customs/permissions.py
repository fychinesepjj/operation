import logging
from django.db.models import get_models
from django.utils.encoding import smart_unicode
from django.db.models.signals import post_syncdb
from django.contrib.auth import models as auth_app

from operation.core.models.base import PermissionReadonlyView

logger = logging.getLogger('django')


def _get_permission_codename(action, opts):
    return u'%s_%s' % (action, opts.object_name.lower())


def _get_all_permissions(opts, actions):
    "Returns (codename, name) for all permissions in the given opts."
    perms = []
    for action in actions:
        perms.append(
            (_get_permission_codename(action, opts), u'Can %s %s' %
             (action, opts.verbose_name_raw)))
    return perms


def _get_default_permissions(opts):
    return _get_all_permissions(opts, ('add', 'change', 'delete', 'view'))


def _get_sync_to_permissions(opts):
    return _get_all_permissions(opts, ('sync_to',))


def _get_sync_from_permissions(opts):
    return _get_all_permissions(opts, ('sync_from',))


def create_permissions_respecting_proxy(app, created_models, verbosity, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from operation.core.models.base import BaseSyncModel

    app_models = get_models(app)

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for klass in app_models:
        ctype, created = ContentType.objects.get_or_create(
            app_label=klass._meta.app_label,
            model=klass._meta.module_name,
            defaults={
                'name': smart_unicode(klass._meta.verbose_name_raw)
            }
        )
        ctypes.add(ctype)
        for perm in _get_default_permissions(klass._meta):
            searched_perms.append((ctype, perm))
        # only support sync_to perms for BaseSyncModel
        if issubclass(klass, BaseSyncModel):
            for perm in _get_sync_to_permissions(klass._meta):
                searched_perms.append((ctype, perm))

    # Find all the Permissions that have a context_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(auth_app.Permission.objects.filter(content_type__in=ctypes).values_list("content_type", "codename"))

    for ctype, (codename, name) in searched_perms:
        # If the permissions exists, move on.
        if (ctype.pk, codename) in all_perms:
            continue
        print 'Create perm: %s' % codename
        p = auth_app.Permission.objects.create(
            codename=codename,
            name=name,
            content_type=ctype
        )
        if verbosity >= 2:
            print "Adding permission '%s'" % p


# check for all model to create extra permissions after a syncdb
from django.contrib.auth.management import create_permissions
post_syncdb.disconnect(create_permissions, dispatch_uid='django.contrib.auth.management.create_permissions')
post_syncdb.connect(create_permissions_respecting_proxy, dispatch_uid='django.contrib.auth.management.create_permissions')


#dynamic check view permission actions
def check_view_readonly_action(obj):
    bool_list = []
    if not isinstance(obj, PermissionReadonlyView):
        return False

    action_items = obj.get_view_readonly_actions()
    if not action_items:
        return False

    for func in action_items:
        if callable(func):
            try:
                bool_list.append(func(obj))
            except Exception as e:
                logger.error(e)
                bool_list.append(False)
    if bool_list:
        return all(bool_list)
    else:
        return False


# Dynamic check fields permission actions
def check_fields_readonly_action(obj):
    '''
    bool_list = []
    if not isinstance(obj, PermissionReadonlyFields):
        return False
    action_items = obj.get_fields_readonly_actions()
    To be continue
    '''
    return False
