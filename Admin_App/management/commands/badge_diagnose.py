from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from Admin_App.models import PropertyBadge
from Admin_App.badge_utils import get_badged_objects, BADGE_META


class Command(BaseCommand):
    help = "Explains why each saved badge is (or is not) showing on the website."

    def handle(self, *args, **opts):
        today = timezone.localdate()
        rows = PropertyBadge.objects.select_related("content_type").order_by("-created_at")
        self.stdout.write(f"Total badge rows in DB: {rows.count()}  (today = {today})\n")
        for b in rows:
            model = b.content_type.model_class()
            obj = model.objects.filter(pk=b.object_id).first() if model else None
            problems = []
            if not b.is_active:
                problems.append("badge is switched OFF")
            if b.start_date and b.start_date > today:
                problems.append(f"starts in future ({b.start_date})")
            if b.end_date and b.end_date < today:
                problems.append(f"already expired ({b.end_date})")
            if model is None:
                problems.append("model class missing")
            elif obj is None:
                problems.append("property not found in DB")
            else:
                if getattr(obj, "is_deleted", False):
                    problems.append("property is deleted")
                if getattr(obj, "approval_status", "Approved") != "Approved":
                    problems.append(f"property approval_status = '{obj.approval_status}' (must be 'Approved')")
            status = "OK -> will show" if not problems else "NOT SHOWING: " + "; ".join(problems)
            self.stdout.write(f"[{b.badge_type:<9}] {b.object_id:<16} {status}")
        self.stdout.write("")
        for key in BADGE_META:
            n = len(get_badged_objects(key))
            self.stdout.write(f"Home section '{key}': {n} property(ies) will appear")