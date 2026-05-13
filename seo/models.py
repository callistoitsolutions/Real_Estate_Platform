from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LocationSEO(models.Model):

    key = models.CharField(max_length=250, unique=True)

    pagetype = models.CharField(max_length=50)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    meta_title = models.CharField(max_length=255)

    meta_description = models.TextField()

    primary_keyword = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    secondary_keywords = models.TextField(
        blank=True,
        null=True
    )

    slug = models.SlugField(
        max_length=300,
        blank=True,
        null=True
    )

    canonical_url = models.URLField(
        blank=True,
        null=True
    )

    schema_json = models.TextField(
        blank=True,
        null=True
    )

    intro_html = models.TextField(
        blank=True,
        null=True
    )

    noindex = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    #created_at = models.DateTimeField()

    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meta_title