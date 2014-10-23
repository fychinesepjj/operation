from grappelli.views.related import AutocompleteLookup
from operation.core.utils import site


class FilteredAutocompleteLookup(AutocompleteLookup):
    """ Patch grappelli's autocomplete to let us control the queryset
    by creating a autocomplete_queryset function on the model """

    def get_queryset(self):
        try:
            if self.model in site._registry:
                qs = site._registry[self.model].queryset(self.request)
            else:
                qs = qs = super(AutocompleteLookup, self).get_queryset()
        except:
            qs = qs = super(AutocompleteLookup, self).get_queryset()
        qs = self.get_filtered_queryset(qs)
        qs = self.get_searched_queryset(qs)
        return qs.distinct()
