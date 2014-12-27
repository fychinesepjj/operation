from django.db import models
from django.utils.translation import ugettext_lazy as _
from operation.core.utils import User


#base object
class PermissionReadonly(object):
    def __init__(self):
        self._added_actions = set()
        self._removed_actions = set()


class PermissionReadonlyView(PermissionReadonly):

    def get_view_readonly_actions(self):
        return self._added_actions - self._removed_actions

    def add_view_readonly_action(self, action):
        self._added_actions.add(action)

    def remove_view_readonly_action(self, action):
        self._removed_actions.add(action)


class PermissionReadonlyFields(PermissionReadonly):
    pass


#django base models
class BaseModel(models.Model):
    creator = models.ForeignKey(User, verbose_name=_("creator"), related_name="+")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    modifier = models.ForeignKey(User, verbose_name=_("modifier"), related_name="+")
    modified_time = models.DateTimeField(auto_now=True, verbose_name=_("last modified"))

    class Meta:
        abstract = True
        ordering = ['-created_time']


class BaseSyncModel(BaseModel):
    published = models.BooleanField(default=True, verbose_name=_("published"))
    sync_status = models.BooleanField(default=False, verbose_name=_("sync status"))

    class Meta:
        abstract = True


from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver


@receiver(pre_delete, dispatch_uid='before_delete_online_info')
def before_delete_online_info(sender, instance, using, **kwargs):
    if issubclass(sender, BaseSyncModel):
        from operationcore.datasync.sync import sync_obj
        sync_obj(instance, sender, up=False, testing=True)
        sync_obj(instance, sender, up=False, testing=False)
    if hasattr(instance, 'before_delete'):
        instance.before_delete(**kwargs)


@receiver(post_delete, dispatch_uid='after_delete_online_info')
def after_delete_online_info(sender, instance, using, **kwargs):
    if hasattr(instance, 'after_delete'):
        instance.after_delete(**kwargs)
