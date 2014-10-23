from fnmatch import fnmatch

from operation.core.utils import site
from django.core.urlresolvers import reverse

full_name = lambda model: '%s.%s' % (model.__module__, model.__name__)


def reverse_menu_list(menu_list):
    models_list = {}
    for app, item in menu_list.iteritems():
        app_title = item.get('title', None)
        app_order = item.get('order', 999)
        models = item.get('models', {})
        for m, m_item in models.iteritems():
            m_title = m_item.get('title', None)
            m_order = m_item.get('order', 999)
            if m not in models_list:
                models_list[m] = {
                    'app_title': app_title,
                    'app_order': app_order,
                    'app_name': app,
                    'title': m_title,
                    'order': m_order,
                }
    return models_list


def get_admin_site_name(context):
    return site.name


def get_avail_models(request):
    """ Returns (model, perm, model_path) for all models user can possibly see """
    items = []
    admin_site = site

    for model, model_admin in admin_site._registry.items():
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            continue
        model_path = full_name(model)
        items.append((model, perms, model_path))
    return items


def filter_models(request, models, exclude):
    """
    Returns (model, perm, model_path) for all models that match models/exclude patterns
    and are visible by current user.
    """
    items = get_avail_models(request)
    included = []

    # I beleive that that implemented
    # O(len(patterns)*len(matched_patterns)*len(all_models))
    # algorythm is fine for model lists because they are small and admin
    # performance is not a bottleneck. If it is not the case then the code
    # should be optimized.

    if len(models) == 0:
        included = items
    else:
        for pattern in models:
            pattern_items = []
            for item in items:
                model, perms, model_path = item
                if fnmatch(model_path, pattern) and item not in included:
                    new_item = model, perms, pattern
                    pattern_items.append(new_item)
            pattern_items.sort(key=lambda x: x[0]._meta.verbose_name_plural)
            included.extend(pattern_items)

    result = included[:]
    for pattern in exclude:
        for item in included:
            model, perms, model_path = item
            if fnmatch(model_path, pattern):
                try:
                    result.remove(item)
                except ValueError:  # if the item was already removed skip
                    pass
    return result


class AppListElementMixin(object):
    """
    Mixin class used by Menu
    """

    def __init__(self, models=tuple(), exclude=tuple()):
        self.models = models
        self.exclude = exclude

    def _visible_models(self, request):
        included = self.models[:]
        excluded = self.exclude[:]
        if not self.models and not self.exclude:
            included = ["*"]
        return filter_models(request, included, excluded)

    def _get_admin_app_list_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:app_list' % get_admin_site_name(context),
                       args=(app_label,))

    def _get_admin_change_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_changelist' % (get_admin_site_name(context),
                                                app_label,
                                                model.__name__.lower()))

    def _get_admin_add_url(self, model, context):
        """
        Returns the admin add url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_add' % (get_admin_site_name(context),
                                         app_label,
                                         model.__name__.lower()))

    def _get_admin_view_url(self, model, context):
        """
        Returns the admin viewlist url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_viewlist' % (get_admin_site_name(context),
                                              app_label,
                                              model.__name__.lower()))
