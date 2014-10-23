from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from operation.core.admin.base import BaseModelAdmin
from operation.core.utils import site

'''
from operation.core.constants import VIEW_CODENAME
class ViewPerm(object):

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        view_permission = VIEW_CODENAME % self.model._meta.module_name
        return request.user.has_perm(opts.app_label + '.' + view_permission)

    def get_model_perms(self, request):
        perms = super(ViewPerm, self).get_model_perms(request)
        perms.update({'view': self.has_view_permission(request)})
        return perms
'''


class UserAdmin2(BaseModelAdmin, UserAdmin):
    inherit_from_basemodel = False


class GroupAdmin2(BaseModelAdmin, GroupAdmin):
    inherit_from_basemodel = False

site.unregister(User)
site.unregister(Group)


site.register(User, UserAdmin2)
site.register(Group, GroupAdmin2)
