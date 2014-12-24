from django.db import models
from django.utils.translation import ugettext_lazy as _
from operation.core.models.base import BaseModel
from constants import FOOTER_CATEGORY
from DjangoUeditor.models import UEditorField


class Site(BaseModel):
    name = models.CharField(verbose_name=_('Site Name'), max_length=256)
    domain = models.CharField(verbose_name=_('Site Domain'), max_length=128)
    logo = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('Logo'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    qr_code = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('QR Code'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    qr_link = models.CharField(verbose_name=_('QR Link'), max_length=128)
    qr_name = models.CharField(verbose_name=_('QR Name'), max_length=64)
    copy_right = models.CharField(verbose_name=_('Copy Right'), max_length=256)
    owner = models.CharField(verbose_name=_('Owner'), max_length=64, blank=True)
    phone = models.CharField(verbose_name=_('Phone'), max_length=64, blank=True)
    address = models.CharField(verbose_name=_('Address'), max_length=256, blank=True)
    introduction = UEditorField(
        verbose_name=_('Site introduction'),
        width=800,
        height=300,
        toolbars="full",
        imagePath="images",
        filePath="files",
        upload_settings={"imageMaxSize": 1204000},
        settings={},
        command=None,
        blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Backend Site')
        verbose_name_plural = _('Backend Sites')


class FooterCategory(BaseModel):
    name = models.CharField(verbose_name=_('Footer Item Name'), max_length=128)
    link = models.CharField(verbose_name=_('Footer Item Link'), max_length=256, blank=True)
    level = models.IntegerField(verbose_name=_('level'), choices=FOOTER_CATEGORY.to_choices())
    icon_class = models.CharField(verbose_name=_('Footer Icon class'), max_length=64, blank=True)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        limit_choices_to={'level__exact': FOOTER_CATEGORY.ROOT},
        null=True,
        blank=True,
        verbose_name=_('parent'))
    ordering = models.PositiveIntegerField(_('ordering'), default=1)

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains")

    def related_label(self):
        return u"%s (%s)" % (self.name, self.id)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Footer Category')
        verbose_name_plural = _('Footer Category')


class Project(BaseModel):
    title = models.CharField(verbose_name=_('Project Title'), max_length=256)
    content = UEditorField(
        verbose_name=_('Project Content'),
        width=800,
        height=300,
        toolbars="full",
        imagePath="images",
        filePath="files",
        upload_settings={"imageMaxSize": 1204000},
        settings={},
        command=None,
        blank=True)
    image = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('Project Image'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    ordering = models.PositiveIntegerField(_('ordering'), default=1)
    promote = models.BooleanField(default=False, verbose_name=_("Promote"))

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Team(BaseModel):
    title = models.CharField(verbose_name=_('Team Title'), max_length=256)
    sub_title = models.CharField(verbose_name=_('Team Sub Title'), max_length=256)
    ordering = models.PositiveIntegerField(_('ordering'), default=1)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')


class Member(BaseModel):
    team = models.ForeignKey(Team, related_name='members', verbose_name=_('Relate team'))
    name = models.CharField(verbose_name=_('Member Name'), max_length=64)
    career = models.CharField(verbose_name=_('Career'), max_length=128)
    title = models.CharField(verbose_name=_('title'), max_length=256)
    content = UEditorField(
        verbose_name=_('Member About'),
        width=800,
        height=300,
        toolbars="full",
        imagePath="images",
        filePath="files",
        upload_settings={"imageMaxSize": 1204000},
        settings={},
        command=None,
        blank=True)
    portrait = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('Portrait'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    ordering = models.PositiveIntegerField(_('ordering'), default=1)

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", "career__icontains")

    def related_label(self):
        return u"%s (%s)" % (self.name, self.id)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')


class Home(BaseModel):
    name = models.CharField(verbose_name=_('Home Name'), max_length=128)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = _('Home Page')
        verbose_name_plural = _('Home Page')


class NavGuide(BaseModel):
    name = models.CharField(verbose_name=_('Guide Name'), max_length=128)
    link = models.CharField(verbose_name=_('Guide Link'), max_length=128)
    image = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('Guide Image'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    title = models.CharField(verbose_name=_('Guide Title'), max_length=256)
    sub_title = models.CharField(verbose_name=_('Guide Sub Title'), max_length=256)
    home = models.OneToOneField("Home", verbose_name=_('Home Page'), related_name="navguide")

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name = _('Nav Guide')
        verbose_name_plural = _('Nav Guide')


class NavList(BaseModel):
    image = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('List Image'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    title = models.CharField(verbose_name=_('Nav Title'), max_length=256)
    sub_title = models.CharField(verbose_name=_('Nav Sub Title'), max_length=256)
    home = models.ForeignKey("Home", verbose_name=_('Home Page'), related_name="navlist")

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name = _('Nav List')
        verbose_name_plural = _('Nav List')
