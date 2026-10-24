"""
Property badge helpers (Featured / Sponsored / Verified / Exclusive / Popular / Latest).
Badges live in ONE generic model (PropertyBadge) so all 11 property models are covered
without touching any of them.
"""
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import traceback

# 0 = only badges set from the admin panel. Set e.g. 7 to auto-show "Latest" on listings < 7 days old.
AUTO_LATEST_DAYS = 0

BADGE_META = {
    "featured":  {"label": "Featured",  "icon": "bi bi-star-fill",          "bg": "#f59e0b", "fg": "#ffffff", "order": 1},
    "sponsored": {"label": "Sponsored", "icon": "bi bi-megaphone-fill",     "bg": "#7c3aed", "fg": "#ffffff", "order": 2},
    "verified":  {"label": "Verified",  "icon": "bi bi-patch-check-fill",   "bg": "#16a34a", "fg": "#ffffff", "order": 3},
    "exclusive": {"label": "Exclusive", "icon": "bi bi-gem",                "bg": "#111827", "fg": "#facc15", "order": 4},
    "popular":   {"label": "Popular",   "icon": "bi bi-fire",               "bg": "#ef4444", "fg": "#ffffff", "order": 5},
    "latest":    {"label": "Latest",    "icon": "bi bi-lightning-charge-fill", "bg": "#2563eb", "fg": "#ffffff", "order": 6},
}
BADGE_CHOICES = [(k, v["label"]) for k, v in BADGE_META.items()]


def all_property_models():
    from Admin_App.models import (
        RentalResidentialProperty, CommercialRentalProperty, PGColivingProperty,
        ResaleResidentialProperty, CommercialResaleProperty, IndustrialResaleProperty,
        AgriculturalResaleProperty, ResidentialPlotResaleProperty, CommercialPlotResaleProperty,
        IndustrialPlotResaleProperty, AgriculturalPlotResaleProperty,
    )
    return [
        RentalResidentialProperty, CommercialRentalProperty, PGColivingProperty,
        ResaleResidentialProperty, CommercialResaleProperty, IndustrialResaleProperty,
        AgriculturalResaleProperty, ResidentialPlotResaleProperty, CommercialPlotResaleProperty,
        IndustrialPlotResaleProperty, AgriculturalPlotResaleProperty,
    ]


def live_q(prefix=""):
    """Q for badges that are active and inside their (optional) date window."""
    today = timezone.localdate()
    p = prefix
    return (Q(**{p + "is_active": True})
            & (Q(**{p + "start_date__isnull": True}) | Q(**{p + "start_date__lte": today}))
            & (Q(**{p + "end_date__isnull": True}) | Q(**{p + "end_date__gte": today})))


def _meta(key):
    m = dict(BADGE_META[key])
    m["key"] = key
    return m


def _sorted_unique(keys):
    keys = sorted(set(k for k in keys if k in BADGE_META), key=lambda k: BADGE_META[k]["order"])
    return [_meta(k) for k in keys]


def _auto_latest(obj):
    if not AUTO_LATEST_DAYS:
        return False
    created = getattr(obj, "created_at", None)
    return bool(created and timezone.now() - created < timedelta(days=AUTO_LATEST_DAYS))


def get_badges_for(obj):
    """Badges for one property object -> list of meta dicts."""
    from Admin_App.models import PropertyBadge
    try:
        ct = ContentType.objects.get_for_model(obj)
        keys = list(PropertyBadge.objects.filter(live_q(), content_type=ct, object_id=str(obj.pk))
                    .values_list("badge_type", flat=True))
    except Exception:
        traceback.print_exc()   # was silent before - now visible in the server console
        keys = []
    if _auto_latest(obj):
        keys.append("latest")
    return _sorted_unique(keys)


def get_badge_map(objs):
    """Bulk version. objs = list of property objects -> {(model_label, str(pk)): [meta,...]}"""
    from Admin_App.models import PropertyBadge
    objs = list(objs)
    result = {}
    by_model = {}
    for o in objs:
        by_model.setdefault(o.__class__, []).append(o)
    for model, items in by_model.items():
        try:
            ct = ContentType.objects.get_for_model(model)
            rows = PropertyBadge.objects.filter(
                live_q(), content_type=ct, object_id__in=[str(i.pk) for i in items]
            ).values_list("object_id", "badge_type")
            tmp = {}
            for oid, bt in rows:
                tmp.setdefault(oid, []).append(bt)
        except Exception:
            traceback.print_exc()
            tmp = {}
        for i in items:
            keys = list(tmp.get(str(i.pk), []))
            if _auto_latest(i):
                keys.append("latest")
            result[(model._meta.label_lower, str(i.pk))] = _sorted_unique(keys)
    return result


def badges_from_map(badge_map, obj):
    return badge_map.get((obj.__class__._meta.label_lower, str(obj.pk)), [])


def get_badges_by_ids(ids):
    """For the listing page where only dicts (with ids) exist -> {str(id): [meta,...]}"""
    from Admin_App.models import PropertyBadge
    ids = [str(i) for i in ids]
    out = {}
    try:
        for oid, bt in PropertyBadge.objects.filter(live_q(), object_id__in=ids).values_list("object_id", "badge_type"):
            out.setdefault(oid, []).append(bt)
    except Exception:
        traceback.print_exc()
    return {k: _sorted_unique(v) for k, v in out.items()}


def get_badged_objects(badge_type, limit=8):
    """Approved, non-deleted property objects holding a live badge of this type
    (highest priority first, then newest assignment)."""
    from Admin_App.models import PropertyBadge
    rows = list(PropertyBadge.objects.filter(live_q(), badge_type=badge_type)
                .select_related("content_type").order_by("-priority", "-created_at")[: limit * 3])
    grouped = {}
    for r in rows:
        grouped.setdefault(r.content_type_id, []).append(r.object_id)
    fetched = {}
    for ct_id, pks in grouped.items():
        model = ContentType.objects.get_for_id(ct_id).model_class()
        if model is None:
            continue
        names = {f.name for f in model._meta.get_fields()}
        flt = {"pk__in": pks}
        if "is_deleted" in names:
            flt["is_deleted"] = False
        if "approval_status" in names:
            flt["approval_status"] = "Approved"
        qs = model.objects.filter(**flt)
        if "images" in names:
            qs = qs.prefetch_related("images")
        for o in qs:
            fetched[(ct_id, str(o.pk))] = o
    objs = []
    for r in rows:
        o = fetched.get((r.content_type_id, r.object_id))
        if o is not None:
            objs.append(o)
        if len(objs) >= limit:
            break
    return objs