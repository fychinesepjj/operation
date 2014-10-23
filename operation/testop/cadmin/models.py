from django.db import models
from django.utils.translation import ugettext_lazy as _
from operation.core.models.base import PermissionReadonlyView, BaseSyncModel


class PushMessage(BaseSyncModel):
    name = models.CharField(max_length=20, blank=True)
    content = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Push Message')
        verbose_name_plural = _('Push Messages')
        app_label = 'cadmin'


class Tag(models.Model):
    """docstring for Tags"""
    tag_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "tag_name__icontains",)

    def __unicode__(self):
        return self.tag_name

    def related_label(self):
        return u"%s (%s)" % (self.tag_name, self.id)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        app_label = 'cadmin'


class Author(models.Model):
    """docstring for Author"""
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    def related_label(self):
        return u"%s (%s)" % (self.name, self.id)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        app_label = 'cadmin'


class Blog(models.Model, PermissionReadonlyView):
    """docstring for Blogs"""
    caption = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    tags = models.ManyToManyField(Tag, blank=True)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def get_view_readonly_actions(self):
        self.add_view_readonly_action(self.check_caption)
        return super(Blog, self).get_view_readonly_actions()

    def check_caption(self, *args):
        if self.caption == 'abc':
            return True
        return False

    def __unicode__(self):
        return u'%s %s %s' % (self.caption, self.author, self.publish_time)

    def related_label(self):
        return u"%s (%s)" % (self.caption, self.id)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        app_label = 'cadmin'
