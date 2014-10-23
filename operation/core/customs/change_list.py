from django.contrib.admin.views.main import ChangeList
from django.core.urlresolvers import reverse
from django.contrib.admin.util import quote


class ViewChangeList(ChangeList):

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return reverse('admin:%s_%s_view' % (self.opts.app_label,
                       self.opts.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)
