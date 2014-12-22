from django.db import models
from django.utils.translation import ugettext_lazy as _
from operation.core.models.base import BaseModel


class Site(BaseModel):
    name = models.CharField(verbose_name=_('Site Name'), max_length=64)
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
    introduction = models.TextField(verbose_name=_('Site introduction'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Backend Site')
        verbose_name_plural = _('Backend Sites')


class Footer(BaseModel):
    name = models.CharField(verbose_name=_('Footer Item Name'), max_length=128)
    link = models.CharField(verbose_name=_('Footer Item Link'), max_length=256, blank=True)
    level = models.CharField(verbose_name=_('Footer Item Level'), max_length=20, blank=True)
    icon_class = models.CharField(verbose_name=_('Footer Icon class'), max_length=64, blank=True)
    parent = models.CharField(verbose_name=_('Footer Item parent'), max_length=20, blank=True)
    ordering = models.PositiveIntegerField(_('ordering'), default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Footer')
        verbose_name_plural = _('Footer')


class Project(BaseModel):
    title = models.CharField(verbose_name=_('Project Title'), max_length=256)
    content = models.TextField(verbose_name=_('Project Content'))
    ordering = models.PositiveIntegerField(_('ordering'), default=1)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Team(BaseModel):
    title = models.CharField(max_length=256)
    sub_title = models.CharField(max_length=256)
    ordering = models.PositiveIntegerField(_('ordering'), default=1)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')


class Member(BaseModel):
    name = models.CharField(verbose_name=_('Member Name'), max_length=64)
    introduction = models.TextField(verbose_name=_('Member introduction'))
    portrait = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('Portrait'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    ordering = models.PositiveIntegerField(_('ordering'), default=1)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')


class NavGuide(BaseModel):
    name = models.CharField(verbose_name=_('Guide Name'), max_length=64)
    image = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        verbose_name=_('Guide Image'),
        help_text=_('Please upload JPEG, PNG, GIF files, size: 64x64')
    )
    title = models.CharField(verbose_name=_('Guide Title'), max_length=256)
    sub_title = models.CharField(verbose_name=_('Guide Sub Title'), max_length=256)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = _('NavGuide')
        verbose_name_plural = _('NavGuide')