from operation.core.utils.enum import Enum
from django.utils.translation import ugettext_lazy as _

FOOTER_CATEGORY = Enum([
    ('ROOT', (-1, _('Root'))),
    ('FIRST', (1, _('First'))),
])
