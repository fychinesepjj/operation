from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import Site, FooterCategory, Project, Team, Member, NavGuide, NavList, Home
from operation.core.admin.base import BaseModelAdmin, BaseModelInline
from grappelli.forms import GrappelliSortableHiddenMixin
from operation.core.utils import site


class WebSiteAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'domain', 'copy_right')
    list_display_links = ('id', 'name')
    fieldsets = (
        (_('Basic'), {
            'fields': ('name', 'domain', 'logo', 'copy_right'),
        }),
        (_('User'), {
            'fields': ('owner', 'phone', 'email', 'address'),
        }),
        (_('Info'), {
            'fields': (('qr_name', 'qr_link', 'qr_code', 'introduction')),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
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
    list_editable = ('ordering', 'promote')
    ordering = ('ordering',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('title', 'sub_title', 'image', 'display_style', 'ordering', 'promote', 'content'),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
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


class MemberInlineAdmin(BaseModelInline, GrappelliSortableHiddenMixin, admin.StackedInline):
    model = Member
    '''
    autocomplete_lookup_fields = {
        'fk': ['image'],
    }
    '''
    ordering = ('ordering',)
    inline_classes = ('grp-collapse grp-open grp-closed',)
    fields = ('ordering', 'name', 'career', 'portrait', 'title', 'content')
    sortable_field_name = 'ordering'
    extra = 0


class TeamAdmin(BaseModelAdmin):
    list_display = ('ordering', 'id', 'title', 'created_time')
    list_display_links = ('id', 'title')
    list_editable = ('ordering', )
    ordering = ('ordering',)
    fieldsets = (
        (_('Basic'), {
            'fields': ('title', 'sub_title'),
        }),
        (_("Members"), {
            "classes": ("placeholder members-group", ),
            "fields": (),
        }),
        (_('Other'), {
            'fields': (('created_time', 'modified_time', 'creator', 'modifier')),
        }),
    )
    inlines = [MemberInlineAdmin]


class NavListInline(BaseModelInline, GrappelliSortableHiddenMixin, admin.StackedInline):
    model = NavList
    extra = 1
    max_num = 3
    fields = ('ordering', 'title', 'link', 'sub_title', 'image')
    inline_classes = ('grp-collapse grp-open grp-closed',)
    sortable_field_name = 'ordering'
    extra = 1


class NavGuideInline(BaseModelInline, admin.StackedInline):
    model = NavGuide
    can_delete = False
    max_num = 1
    fields = ('name', 'link', 'title', 'sub_title', 'image', 'slogan_title', 'slogan_sub_title')
    inline_classes = ('grp-collapse grp-open',)


class HomeAdmin(BaseModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ('id',)

    fieldsets = (
        (_('Basic'), {
            'fields': ('name', ),
        }),
        (_("NavGuide Targets"), {
            "classes": ("placeholder navguide-group", ),
            "fields": (),
        }),
        (_("Navlist Targets"), {
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
