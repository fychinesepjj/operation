from operation.core.constants import DEFAULT_GROUP_LABEL_NAME
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.contrib import messages


class BaseGroupAdmin(object):
    __group_field_name = 'group_code'

    def __init__(self):
        self.__errors = []

    @property
    def errors(self):
        return self.__errors

    def clear_errors(self):
        errors = self.__errors
        del errors
        self.__errors = []

    def _check_user_group(self, user):
        user_group_values = user.groups.values()
        if user_group_values:
            g_ids = [g['id'] for g in user_group_values]
            g_ids.sort()
            return g_ids
        else:
            #user attach to default group
            default_group = self._get_default_group()
            default_group.user_set.add(user)
            return [default_group.id]

    def _get_default_group(self):
        from django.contrib.auth.models import Group
        default_group_list = Group.objects.filter(name=DEFAULT_GROUP_LABEL_NAME)
        if default_group_list:
            default_group = default_group_list[0]
            return default_group
        return Group.objects.create(name=DEFAULT_GROUP_LABEL_NAME)

    def _get_group_code(self, request):
        if request.user:
            #get user group code
            group_ids = self._check_user_group(request.user)
            group_ids_str = [str(i) for i in group_ids]
            g_code = ''.join(group_ids_str)
            return g_code

    def _set_group_code(self, obj, g_code):
        if obj and not obj.pk:
            if g_code and hasattr(obj, self.__group_field_name):
                setattr(obj, self.__group_field_name, g_code)
                return True
            else:
                self.__errors.append(_('set <group_code> field is not exists, Please alter db table and add this field.'))
        return False

    def _add_group(self, request, obj):
        g_code = self._get_group_code(request)
        return self._set_group_code(obj, g_code)

    def save_group_model(self, admin, request, obj, form, change):
        if obj and not obj.pk:
            return self._add_group(request, obj)
        return True

    def query_by_group(self, request, queryset):
        group_field_error = False
        if queryset:
            obj = queryset[0]
            if not hasattr(obj, self.__group_field_name):
                group_field_error = True
                self.__errors.append(_('query <group_code> field is not exists, Please alter db table and add this field.'))
        if not queryset or group_field_error:
            return queryset.none()
        g_code = self._get_group_code(request)
        if g_code:
            return queryset.filter(**{self.__group_field_name: g_code})
        return queryset.none()


class QueryFilter(object):

    def query_by_user(self, request, query_set):
        user = request.user
        if user:
            return query_set.filter(creator=user)
        return query_set.none()

    def query_by_superuser(self, request, query_set):
        user = request.user
        if user:
            if user.is_superuser:
                return query_set
            return query_set.filter(creator=user)
        return query_set.none()

    def query_by_group(self, group_admin, request, query_set):
        user = request.user
        if user:
            if user.is_superuser:
                return query_set
            return group_admin.query_by_group(request, query_set)
        return query_set.none()


class AuthManager(object):
    _group_admin = None
    _query_admin = None

    @property
    def group_admin(self):
        if not self._group_admin:
            self._group_admin = BaseGroupAdmin()
            return self._group_admin
        return self._group_admin

    @property
    def query_admin(self):
        if not self._query_admin:
            self._query_admin = QueryFilter()
            return self._query_admin
        return self._query_admin

    def query_by_auth(self, admin, request, ori_query_set):
        query_filter = admin.query_filter
        queryset = ori_query_set.none()
        if query_filter:
            if query_filter == 'group':
                queryset = self.query_admin.query_by_group(self.group_admin, request, ori_query_set)
            elif query_filter == 'user':
                queryset = self.query_admin.query_by_user(request, ori_query_set)
            elif query_filter == 'superuser':
                queryset = self.query_admin.query_by_superuser(request, ori_query_set)
            else:
                queryset = ori_query_set
        if not queryset:
            self._feedback_errors(admin, request)
        return queryset

    def _feedback_errors(self, admin, request):
        if self.group_admin.errors:
            error_list = [force_text(error) for error in self.group_admin.errors]
            errors_str = ','.join(error_list)
            admin.message_user(request, errors_str, messages.ERROR)
            self.group_admin.clear_errors()

    def save_group_model(self, admin, request, obj, form, change):
        query_filter = admin.query_filter
        if query_filter and query_filter == 'group':
            status = self.group_admin.save_group_model(admin, request, obj, form, change)
            if not status:
                self._feedback_errors(admin, request)
            return status
        return False

auth_manager = AuthManager()
