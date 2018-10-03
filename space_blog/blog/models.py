import requests

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    caption = models.CharField(max_length=256, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'caption',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


class BlogIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        posts = BlogPage.objects.live().order_by('-date')
        posts_count = posts.count

        # Only get first 5 posts ordered by date created
        posts_list = posts[:5]

        context['posts'] = posts_list
        context['posts_count'] = posts_count

        return context


class BlogPage(Page):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('missions', 'Missions'),
        ('politics', 'Politics'),
        ('discoveries', 'Discoveries'),
    ]

    date = models.DateField("Post date")
    category = models.CharField(
        max_length=256,
        choices=CATEGORY_CHOICES,
    )
    subtitle = models.CharField(blank=True, max_length=256)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('blockquote', blocks.BlockQuoteBlock()),
        ('image', ImageChooserBlock()),
    ])

    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('subtitle'),
        FieldPanel('category'),
        StreamFieldPanel('body'),
    ]