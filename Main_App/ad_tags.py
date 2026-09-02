from django import template
from django.utils import timezone
from django.db.models import F
from Main_App.models import BrandAd

register = template.Library()

@register.inclusion_tag('ads/_ad_slot.html')
def render_ad_slot(placement, limit=5):
    today = timezone.localdate()
    ads = list(
        BrandAd.objects.filter(
            placement=placement,
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        ).order_by('-priority')[:limit]
    )
    if ads:
        BrandAd.objects.filter(pk__in=[a.pk for a in ads]).update(impressions=F('impressions') + 1)
    return {'ads': ads, 'placement': placement}