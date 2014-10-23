from django.contrib import admin
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.http import Http404


class CustomAdminSite(admin.sites.AdminSite):

    def unregister(self, model_or_iterable):
        valid_models = []
        if isinstance(model_or_iterable, list):
            for model in model_or_iterable:
                if self.check_exist(model):
                    valid_models.append(model)
        else:
            if self.check_exist(model_or_iterable):
                valid_models.append(model_or_iterable)
        super(CustomAdminSite, self).unregister(valid_models)

    def check_exist(self, model):
        if model not in self._registry:
            return False
        return True

    def app_index(self, request, app_label, extra_context=None):
        user = request.user
        has_module_perms = user.has_module_perms(app_label)
        app_dict = {}
        for model, model_admin in self._registry.items():
            if app_label == model._meta.app_label:
                if has_module_perms:
                    perms = model_admin.get_model_perms(request)

                    # Check whether user has any perm for this module.
                    # If so, add the module to the model_list.
                    if True in perms.values():
                        info = (app_label, model._meta.model_name)
                        model_dict = {
                            'name': capfirst(model._meta.verbose_name_plural),
                            'object_name': model._meta.object_name,
                            'perms': perms,
                        }
                        try:
                            change_perm = perms.get('change', False)
                            view_perm = perms.get('view', False)

                            if change_perm:
                                admin_url = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                            elif view_perm:
                                admin_url = reverse('admin:%s_%s_viewlist' % info, current_app=self.name)
                            model_dict['admin_url'] = admin_url
                        except NoReverseMatch:
                            pass

                        if perms.get('add', False):
                            try:
                                model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                            except NoReverseMatch:
                                pass
                        if app_dict:
                            app_dict['models'].append(model_dict),
                        else:
                            app_dict = {
                                'name': app_label.title(),
                                'app_label': app_label,
                                'app_url': '',
                                'has_module_perms': has_module_perms,
                                'models': [model_dict],
                            }
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['name'])
        context = {
            'title': _('%s administration') % capfirst(app_label),
            'app_list': [app_dict],
        }
        context.update(extra_context or {})

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context, current_app=self.name)

custom_site = CustomAdminSite()
