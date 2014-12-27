from operation.core.constants import VIEW_CODENAME, SYNCTO_CODENAME, SYNCFROM_CODE
from functools import update_wrapper, partial
from operation.core.customs.permissions import check_view_readonly_action
from operation.core.datasync.sync import sync_obj
from operation.core.customs.forms import PermissionReadonlyForm
from operation.core.admin.manager import auth_manager

from django import forms
from django.db import transaction
from django.contrib import admin
from django.contrib import messages
from django.utils.html import escape
from django.utils.encoding import force_text
from django.forms.models import modelform_factory, modelform_defines_fields
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.contrib.admin.util import model_ngettext
from django.contrib.admin.util import unquote
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ungettext
from django.contrib.admin.options import IS_POPUP_VAR, IncorrectLookupParameters


class BaseModelInline(object):
    extra = 1
    exclude = ('creator', 'created_time', 'modifier', 'modified_time')
    ordering = ['-created_time', ]


class BaseModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected_items']
    inherit_from_basemodel = True
    query_filter = 'none'

    def __init__(self, model, admin_site):
        self.set_admin_fields()
        super(BaseModelAdmin, self).__init__(model, admin_site)

    def set_admin_fields(self):
        if self.inherit_from_basemodel:
            self.set_readonly_fields()
            self.set_ordering_fields()

    def set_ordering_fields(self):
        base_ordering_fields = ['-created_time']
        if self.ordering:
            self.ordering = list(self.ordering) + base_ordering_fields
        else:
            self.ordering = base_ordering_fields

    def set_readonly_fields(self):
        base_readonly_fields = ['creator', 'created_time', 'modifier', 'modified_time']
        if self.readonly_fields:
            self.readonly_fields += base_readonly_fields
        else:
            self.readonly_fields = base_readonly_fields

    def save_formset(self, request, form, formset, change):
        if request.method == "POST":
            objs = formset.save(commit=False)
            for obj in objs:
                if not obj.pk and self.inherit_from_basemodel:
                    if not hasattr(obj, 'creator'):
                        obj.creator = request.user
                    obj.modifier = request.user
                obj.save()
            formset.save_m2m()

    def get_actions(self, request):
        actions = super(BaseModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if not self.has_delete_permission(request) and 'delete_selected_items' in actions:
            del actions['delete_selected_items']
        return actions

    def delete_selected_items(self, request, queryset):
        n = queryset.count()
        if n:
            for obj in queryset:
                self.log_deletion(request, obj, force_unicode(obj))
                obj.delete()
            self.message_user(request, _('Successfully deleted %(count)d %(items)s.') % {
                'count': n, 'items': model_ngettext(self.opts, n)
            })
    delete_selected_items.short_description = _('Delete selected %(verbose_name_plural)s')

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        urlpatterns = patterns(
            '',
            url(r'^viewlist/$', wrap(self.changelist_readonly_view), name='%s_%s_viewlist' % info),
            url(r'^(.+)/view/$', wrap(self.readonly_view), name='%s_%s_view' % info),
        )
        org_patterns = super(BaseModelAdmin, self).get_urls()
        urlpatterns += org_patterns
        return urlpatterns

    @csrf_protect_m
    @transaction.atomic
    def readonly_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        opts = model._meta
        obj = self.get_object(request, unquote(object_id))
        if not self.has_view_permission(request, obj):
            raise PermissionDenied
        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_text(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST':
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        elif request.method == 'GET':
            # Create a new var used in render_change_form for judgement
            if extra_context:
                extra_context.update({'readonly': True})
            else:
                extra_context = {'readonly': True}

            ModelForm = self.get_form(request, obj)
            formsets = []
            inline_instances = self.get_inline_instances(request, obj)
            form = ModelForm(instance=obj)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, obj), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.get_queryset(request))
                formsets.append(formset)

            adminForm = helpers.AdminForm(
                form,
                self.get_fieldsets(request, obj),
                self.get_prepopulated_fields(request, obj),
                self.get_readonly_fields(request, obj),
                model_admin=self
            )
            media = self.media + adminForm.media

            inline_admin_formsets = []
            for inline, formset in zip(inline_instances, formsets):
                fieldsets = list(inline.get_fieldsets(request, obj))
                readonly = list(inline.get_readonly_fields(request, obj))
                prepopulated = dict(inline.get_prepopulated_fields(request, obj))
                inline_admin_formset = helpers.InlineAdminFormSet(
                    inline,
                    formset,
                    fieldsets,
                    prepopulated,
                    readonly,
                    model_admin=self
                )
                inline_admin_formsets.append(inline_admin_formset)
                media = media + inline_admin_formset.media

            context = {
                'title': _('View %s') % force_text(opts.verbose_name),
                'adminform': adminForm,
                'object_id': object_id,
                'original': obj,
                'is_popup': IS_POPUP_VAR in request.REQUEST,
                'media': media,
                'inline_admin_formsets': inline_admin_formsets,
                'errors': helpers.AdminErrorList(form, formsets),
                'app_label': opts.app_label,
                'preserved_filters': self.get_preserved_filters(request),
            }
            context.update(extra_context or {})
            return self.render_change_form(request, context, change=False, obj=obj, form_url=form_url)
        else:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_text(opts.verbose_name), 'key': escape(object_id)})

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if 'readonly' not in context:
            context.update({'readonly': False})
        else:
            add = False
            change = False
        opts = self.model._meta
        app_label = opts.app_label
        form_url = ''
        context.update({
            'add': add,
            'change': change,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_view_permission': self.has_view_permission(request, obj),
            'has_file_field': True,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'form_url': form_url,
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': False,
            'save_on_top': False,
        })

        add_change_search_list = [
            "admin/%s/%s/change_form.html" % (app_label, opts.model_name),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ]
        tml_search_list = add_change_search_list

        form_template = None
        if add and self.add_form_template is not None:
            form_template = self.add_form_template
        elif change and self.change_form_template is not None:
            form_template = self.change_form_template
        return TemplateResponse(request, form_template or tml_search_list, context, current_app=self.admin_site.name)

    @csrf_protect_m
    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        opts = model._meta
        obj = self.get_object(request, unquote(object_id))
        readonly_permission_status = check_view_readonly_action(obj)
        redirect_url = reverse('admin:%s_%s_view' %
                               (opts.app_label, opts.model_name),
                               args=(object_id,),
                               current_app=self.admin_site.name)

        if not self.has_change_permission(request, obj):
            if not self.has_view_permission(request, obj):
                raise PermissionDenied
            else:
                return HttpResponseRedirect(redirect_url)

        if readonly_permission_status:
            return HttpResponseRedirect(redirect_url)
        return super(BaseModelAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_view_chanagelist(self, request, **kwargs):
        from operation.core.customs.change_list import ViewChangeList
        '''
        custome ViewChangeList used for view page
        '''
        return ViewChangeList

    @csrf_protect_m
    def changelist_readonly_view(self, request, extra_context=None):
        from django.contrib.admin.views.main import ERROR_FLAG
        opts = self.model._meta
        app_label = opts.app_label

        if not self.has_view_permission(request, None):
            raise PermissionDenied

        list_display = self.get_list_display(request)
        list_display_links = list(list_display)[:1]
        list_filter = self.get_list_filter(request)
        action_form = None
        cl = None

        ChangeList = self.get_view_chanagelist(request)
        try:
            cl = ChangeList(
                request,
                self.model,
                list_display,
                list_display_links, list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                self.list_per_page, self.list_max_show_all, self.list_editable,
                self
            )
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')
        cl.formset = None
        selection_note_all = ungettext(
            '%(total_count)s selected',
            'All %(total_count)s selected', cl.result_count
        )

        context = {
            'module_name': force_text(opts.verbose_name_plural),
            'selection_note': _('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
            'selection_note_all': selection_note_all % {'total_count': cl.result_count},
            'title': cl.title,
            'is_popup': IS_POPUP_VAR in request.REQUEST,
            'cl': cl,
            'media': self.media,
            'has_add_permission': self.has_add_permission(request),
            'opts': cl.opts,
            'app_label': app_label,
            'action_form': action_form,
            'actions_on_top': False,
            'actions_on_bottom': False,
            'actions_selection_counter': self.actions_selection_counter,
            'preserved_filters': self.get_preserved_filters(request),
        }
        context.update(extra_context or {})

        return TemplateResponse(request, [
            'admin/%s/%s/change_list.html' % (app_label, opts.model_name),
            'admin/%s/change_list.html' % app_label,
            'admin/change_list.html'
        ], context, current_app=self.admin_site.name)

    def get_changelist_form(self, request, **kwargs):
        """
        Returns a Form class for use in the Formset on the changelist page.
        """
        defaults = {
            "formfield_callback": partial(self.formfield_for_dbfield, request=request),
            "form": PermissionReadonlyForm,
        }

        defaults.update(kwargs)
        if (defaults.get('fields') is None and not modelform_defines_fields(defaults.get('form'))):
            defaults['fields'] = forms.ALL_FIELDS

        return modelform_factory(self.model, **defaults)

    def changelist_view(self, request, extra_context=None):
        model = self.model
        opts = model._meta
        if not self.has_change_permission(request, None) and self.has_view_permission(request, None):
            view_url = reverse(
                'admin:%s_%s_viewlist' %
                (opts.app_label, opts.model_name),
                current_app=self.admin_site.name
            )
            return HttpResponseRedirect(view_url)
        return super(BaseModelAdmin, self).changelist_view(request, extra_context=extra_context)

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        view_permission = VIEW_CODENAME % self.model._meta.module_name
        return request.user.has_perm(opts.app_label + '.' + view_permission)

    def get_model_perms(self, request):
        perms = super(BaseModelAdmin, self).get_model_perms(request)
        perms.update({'view': self.has_view_permission(request)})
        return perms

    def save_model(self, request, obj, form, change):
        if self.inherit_from_basemodel:
            if not obj.pk:    # New obj
                obj.creator = request.user
            obj.modifier = request.user

        # Custom save_model
        auth_manager.save_group_model(self, request, obj, form, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        query_set = super(BaseModelAdmin, self).get_queryset(request)
        return auth_manager.query_by_auth(self, request, query_set)

    class Media:
        # Js&css used for customing changelist action
        css = {
            'all': ('/static/changelist/css/actions_button.css',),
        }
        js = ('/static/changelist/js/actions_button.js',)


class BaseSyncModelAdmin(BaseModelAdmin):
    actions = ['sync_selected_items', 'delete_selected_items']

    def set_readonly_fields(self):
        base_readonly_fields = ['sync_status', 'creator', 'created_time', 'modifier', 'modified_time']
        if self.readonly_fields:
            self.readonly_fields += base_readonly_fields
        else:
            self.readonly_fields = base_readonly_fields

    def rearrange_actions(self, old_actions):
        from django.utils.datastructures import SortedDict
        new_actions = []
        for action_name in self.actions:
            if action_name in old_actions:
                name, action = action_name, old_actions[action_name]
                new_actions.append((name, action))
        return SortedDict(new_actions)

    def get_actions(self, request):
        actions = super(BaseSyncModelAdmin, self).get_actions(request)
        if not self.has_sync_to_permission(request) and 'sync_selected_items' in actions:
            del actions['sync_selected_items']
        return self.rearrange_actions(actions)

    def _sync_deleted_items(self, deleted_items):
        pass

    def delete_selected_items(self, request, queryset):
        n = queryset.count()
        deleted_items = list(queryset)
        if n:
            self._sync_deleted_items(deleted_items)
            for obj in queryset:
                self.log_deletion(request, obj, force_unicode(obj))
                obj.delete()

            self.message_user(request, _('Successfully deleted %(count)d %(items)s.') % {
                'count': n, 'items': model_ngettext(self.opts, n)
            })
    delete_selected_items.short_description = _('Delete selected %(verbose_name_plural)s')

    def sync_selected_items(self, request, queryset):
        n = queryset.count()
        fails = []
        reasons = ''
        if n:
            for obj in queryset:
                status, reasons = sync_obj(obj, self.model)
                if not status:
                    fails.append(obj)
            synced_count = n - len(fails)
            self.message_user(request, _('Successfully synced %(count)d %(items)s.') % {
                'count': synced_count, 'items': model_ngettext(self.opts, synced_count)
            }, level=messages.SUCCESS)
        else:
            self.message_user(request, _('0 items synced, Please check sync status.'), level=messages.WARNING)

        if fails:
            fails_count = len(fails)
            ids = ','.join([str(o.id) for o in fails])
            self.message_user(request, _('%(count)d  items fail to sync, id:[%(items)s]') % {
                'count': fails_count,
                'items': ids
            },
                level=messages.ERROR
            )
            if reasons:
                self.message_user(request, _('Fail reasons: %(reasons)s') % {
                    'reasons': reasons,
                },
                    level=messages.ERROR
                )
    sync_selected_items.short_description = _('Sync selected %(verbose_name_plural)s')

    def delete_model(self, request, obj):
        result = super(BaseSyncModelAdmin, self).delete_model(request, obj)
        self._sync_deleted_items([obj])
        return result

    def has_sync_to_permission(self, request, obj=None):
        opts = self.opts
        return (opts.app_label + '.' + self._get_sync_to_permission()) in request.user.get_all_permissions()

    def _get_sync_to_permission(self):
        return SYNCTO_CODENAME % self.opts.object_name.lower()

    def has_sync_from_permission(self, request, obj=None):
        opts = self.opts
        return (opts.app_label + '.' + self._get_sync_from_permission()) in request.user.get_all_permissions()

    def _get_sync_from_permission(self):
        return SYNCFROM_CODE % self.opts.object_name.lower()

    def save_model(self, request, obj, form, change):
        if obj.pk and change:
            obj.sync_status = False
            self.message_user(request, _('%s changed, Please Sync it again.') % obj, level=messages.WARNING)
        super(BaseSyncModelAdmin, self).save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context.update({'has_sync_to_permission': self.has_sync_to_permission(request)})
        extra_context.update({'has_sync_from_permission': self.has_sync_from_permission(request)})
        return super(BaseSyncModelAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_model_perms(self, request):
        perms = super(BaseSyncModelAdmin, self).get_model_perms(request)
        perms.update({'syncto': self.has_sync_to_permission(request)})
        perms.update({'syncfrom': self.has_sync_from_permission(request)})
        return perms
