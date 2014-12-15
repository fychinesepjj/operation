from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from operation.core.admin.base import BaseModelAdmin
from operation.core.utils import site
from django.utils.translation import ugettext_lazy as _

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

_LOG_ACTIONS = {
    ADDITION: _('addition action'),
    CHANGE: _('change action'),
    DELETION: _('deletion action'),
}


class LogEntryAdmin(BaseModelAdmin):
    inherit_from_basemodel = False
    list_per_page = 30
    list_display = (
        'user',
        'content_type',
        'object_repr',
        'action_time',
        'display_action_flag')
    list_filter = ('user', 'action_flag')
    readonly_fields = (
        'user',
        'content_type',
        'object_id',
        'object_repr',
        'action_time',
        'action_flag',
        'change_message')
    search_fields = [
        'user__username',
        'content_type__name',
        'object_id',
        'object_repr']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def display_action_flag(self, obj):
        return _LOG_ACTIONS[obj.action_flag]
    display_action_flag.short_description = _('action flag')


class UserAdmin2(BaseModelAdmin, UserAdmin):
    inherit_from_basemodel = False


class GroupAdmin2(BaseModelAdmin, GroupAdmin):
    inherit_from_basemodel = False

site.unregister(User)
site.unregister(Group)

site.register(LogEntry, LogEntryAdmin)
site.register(User, UserAdmin2)
site.register(Group, GroupAdmin2)
