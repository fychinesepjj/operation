from django.contrib import admin
from models import Tag, Author, Blog, PushMessage
from operation.core.admin.base import BaseModelAdmin, BaseSyncModelAdmin
from operation.testop.datasync import register_sync_model
from operation.core.utils import site


class PushMessageAdmin(BaseSyncModelAdmin):
    list_display = ('id', 'name', 'sync_status', 'published', 'creator', 'created_time', 'modified_time')


class TagAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):

    raw_id_fields = ('author', 'tags',)
    '''
    related_lookup_fields = {
        'fk': ['author'],
        'm2m': ['tags'],
    }
    '''

    autocomplete_lookup_fields = {
        'fk': ['author'],
        'm2m': ['tags'],
    }

    readonly_fields = ("publish_time", 'update_time')
    list_display = ('id', 'caption', 'content')
    list_editable = ('caption', )
    fieldsets = (
        (None, {
            'fields': ('caption', 'content'),
        }),
        ('Flags', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('author',),
        }),
        ('Tags', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('tags',),
        }),
        ('Info', {
            'fields': (('publish_time', 'update_time'),),
        }),
    )

    '''
    class Media:
        js = ('/static/tiny_mce/tiny_mce.js',
              '/static/tinymce_setup/tinymce_setup.js',
                )
    '''


site.register(Tag, TagAdmin)
site.register(Author, AuthorAdmin)
site.register(Blog, BlogAdmin)
site.register(PushMessage, PushMessageAdmin)
register_sync_model(PushMessage)
