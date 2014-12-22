from operationcore.utils.enum import Enum
from django.utils.translation import ugettext_lazy as _

PUSH_CHANNEL = Enum([
    ('GOOGLE', ('google', _('Google'))),
    ('APPLE', ('apple', _('Apple'))),
    ('XIAOMI', ('xiaomi', _('XiaoMi'))),
])

