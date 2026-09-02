from django.contrib import admin
from Admin_App.models import Blog   # <-- replace 'yourapp' with your actual app name
from seo.models import LocationSEO,SeoMetaTag

from django.utils.html import format_html


@admin.register(LocationSEO)
class LocationSEOAdmin(admin.ModelAdmin):
    list_display = ("key", "pagetype", "is_active", "meta_title", "view_link")
    list_filter = ("pagetype", "is_active")
    search_fields = ("key", "meta_title", "primary_keyword", "secondary_keywords")
    readonly_fields = ("view_link",)

    fieldsets = (
        ("SEO Details", {
            "fields": (
                "key",
                "pagetype",
                "meta_title",
                "meta_description",
                "primary_keyword",
                "secondary_keywords",
                "intro_html",
                "schema_json",
                "noindex",
                "is_active",
            )
        }),
        ("Content Relation", {
            "fields": ("content_type", "object_id", "view_link")
        }),
    )

    def view_link(self, obj):
        if obj.key:
            return format_html(
                '<a href="{}" target="_blank">View Landing Page</a>',
                f"/{obj.key}/"
            )
        return "-"
    view_link.short_description = "Landing Page Link"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "reading_time", "date_posted", "preview")
    search_fields = ("title", "author", "category", "content")
    list_filter = ("category", "date_posted")
    readonly_fields = ("preview",)

    fieldsets = (
        ("Blog Info", {
            "fields": ("title", "author", "category", "reading_time", "featured_image")
        }),
        ("Content", {
            "fields": ("content", "preview")
        }),
    )

    def preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-width: 200px;"/>', obj.featured_image.url)
        return "-"
    preview.short_description = "Preview Image"




@admin.register(SeoMetaTag)
class SeoMetaTagAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'meta_title', 'created_at')
    search_fields = ('page_name',)
