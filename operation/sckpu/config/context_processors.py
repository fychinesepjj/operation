from cadmin.models import Site, FooterCategory
from cadmin.constants import FOOTER_CATEGORY


def site_info(request):
    site = Site.objects.get()
    if site:
        return {'site': site}
    return {}


def site_footer(request):
    footer_items = []
    items = FooterCategory.objects.filter(level=FOOTER_CATEGORY.ROOT).order_by('ordering')
    for item in items:
        sub_items = item.children.order_by('ordering')
        item.sub_items = sub_items
        footer_items.append(item)
    return {'footer': footer_items}
