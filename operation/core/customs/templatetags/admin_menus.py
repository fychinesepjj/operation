from operation.core.utils.menus import AppListElementMixin, reverse_menu_list
from django.conf import settings
from django.utils.text import capfirst
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django import template
from django.utils import six

register = template.Library()


@register.simple_tag(takes_context=True)
def admin_top_menu(context):
    APP_MENU_LIST = settings.APP_MENU_LIST
    MODELS_MENU_LIST = reverse_menu_list(APP_MENU_LIST)
    app_modules = AppListElementMixin(MODELS_MENU_LIST.keys())
    request_path = context['request'].path
    default_home = {'title': _('Home'), 'url': '/admin/', 'order': -1, 'models': [], 'highlight': True}
    items = app_modules._visible_models(context['request'])
    registered_models = {}
    apps = {}

    if not registered_models:
        for model, perms, model_path in items:
            if model_path not in registered_models:
                registered_models[model_path] = [(model, perms)]
            else:
                registered_models[model_path].append((model, perms))

    for model_path, model_items in MODELS_MENU_LIST.iteritems():
        if model_path in registered_models:
            app_name = model_items['app_name']
            if app_name not in apps:
                app_title = model_items['app_title']
                app_order = model_items['app_order']
                apps[app_name] = {
                    'title': app_title if app_title else capfirst(app_name.title()),
                    'url': '###',
                    'models': [],
                    'order': app_order,
                }
        else:
            continue
        for model, perms in registered_models[model_path]:
            model_title = model_items.get('title', None)
            model_order = model_items.get('order', 999)

            model_dict = {}
            model_dict['title'] = model_title if model_title else capfirst(model._meta.verbose_name_plural)
            model_dict['order'] = model_order

            if perms['change']:
                model_dict['admin_url'] = app_modules._get_admin_change_url(model, context)
            if perms['add']:
                model_dict['add_url'] = app_modules._get_admin_add_url(model, context)
            if perms['view']:
                model_dict['view_url'] = app_modules._get_admin_view_url(model, context)

            change_url = model_dict.get('admin_url', 'None')
            view_url = model_dict.get('view_url', 'None')
            if request_path.startswith(change_url) or request_path.startswith(view_url):
                apps[app_name]['highlight'] = True
                default_home['highlight'] = False

            apps[app_name]['models'].append(model_dict)

    app_list = list(six.itervalues(apps))
    app_list.sort(key=lambda x: x['order'])
    for app in app_list:
        # sort model list alphabetically
        app['models'].sort(key=lambda i: i['order'])

    #default set home page first
    app_list.insert(0, default_home)
    context['admin_app_list'] = app_list

    tpl = ''
    try:
        tpl = get_template('admin/menu.html')
    except:
        pass
    return tpl.render(context) if tpl else tpl
