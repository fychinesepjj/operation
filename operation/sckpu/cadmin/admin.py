from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import Site, FooterCategory, Project, Team, Member, NavGuide, NavList, Home
from operation.core.admin.base import BaseModelAdmin, BaseModelInline
from operation.core.utils import site


class WebSiteAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'domain', 'copy_right')
    list_display_links = ('id', 'name')
    fieldsets = (
        (_('Basic'), {
            'fields': ('name', 'domain', 'logo', 'copy_right'),
        }),
        (_('User'), {
            'fields': ('owner', 'phone', 'address'),
        }),
        (_('Info'), {
            'fields': (('qr_name', 'qr_link', 'qr_code', 'introduction')),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
    )

    class Media:
        js = ('/static/tiny_mce/tiny_mce.js',
              '/static/tinymce_setup/tinymce_setup.js',
                )


class FooterCategoryAdmin(BaseModelAdmin):
    list_display = ('ordering', 'id', 'name', 'level', 'link', 'icon_class', 'created_time')
    list_display_links = ('id', 'name')
    list_editable = ('ordering', )
    ordering = ('ordering',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('name', 'link', 'icon_class', 'level', 'parent'),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
    )


class ProjectAdmin(BaseModelAdmin):
    list_display = ('ordering', 'id', 'title', 'promote', 'created_time')
    list_display_links = ('id', 'title')
    list_editable = ('ordering', )
    ordering = ('ordering',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('title', 'image', 'content', 'promote'),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
    )

    class Media:
        js = ('/static/tiny_mce/tiny_mce.js',
              '/static/tinymce_setup/tinymce_setup.js',
                )


class MemberAdmin(BaseModelAdmin):
    list_display = ('ordering', 'id', 'name', 'career', 'created_time')
    list_display_links = ('id', 'name')
    list_editable = ('ordering', )
    ordering = ('ordering',)
    raw_id_fields = ('team', )
    fieldsets = (
        (_('Basic'), {
            'fields': ('team', 'name', 'career', 'portrait', 'title', 'content'),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
    )

    class Media:
        js = ('/static/tiny_mce/tiny_mce.js',
              '/static/tinymce_setup/tinymce_setup.js',
                )


class MemberInlineAdmin(BaseModelInline, admin.StackedInline):
    model = Member
    '''
    autocomplete_lookup_fields = {
        'fk': ['image'],
    }
    '''
    inline_classes = ('grp-collapse grp-open',)
    fields = ('name', 'career', 'portrait', 'title', 'content')
    sortable_field_name = 'ordering'
    extra = 1


class TeamAdmin(BaseModelAdmin):
    list_display = ('ordering', 'id', 'title', 'created_time')
    list_display_links = ('id', 'title')
    list_editable = ('ordering', )
    ordering = ('ordering',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('title', 'sub_title'),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
    )
    inlines = [MemberInlineAdmin]


class NavListInline(BaseModelInline, admin.StackedInline):
    model = NavList
    can_delete = False
    max_num = 1
    fields = ('name', 'title', 'sub_title', 'image')
    inline_classes = ('grp-collapse grp-open',)


class NavGuideInline(BaseModelInline, admin.StackedInline):
    model = NavGuide
    can_delete = False
    max_num = 1
    fields = ('title', 'sub_title', 'image')
    inline_classes = ('grp-collapse grp-open',)


class HomeAdmin(BaseModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ('id',)

    fieldsets = (
        (_('Basic'), {
            'fields': ('name'),
        }),
        ("NavGuide Targets", {
            "classes": ("placeholder navguide-group", ),
            "fields": (),
        }),
        ("Navlist Targets", {
            "classes": ("placeholder navlist-group", ),
            "fields": (),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
    )
    inlines = [NavGuideInline, NavListInline]


site.register(Site, WebSiteAdmin)
site.register(Team, TeamAdmin)
site.register(Member, MemberAdmin)
site.register(Project, ProjectAdmin)
site.register(Home, HomeAdmin)
site.register(FooterCategory, FooterCategoryAdmin)

