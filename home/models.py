from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalManyToManyField
from modelcluster.models import ClusterableModel

from wagtail.core.models import Page, Site
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,  MultiFieldPanel, PageChooserPanel, FieldRowPanel, ObjectList, PublishingPanel, TabbedInterface
)
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

class GalleryPhotoForm(WagtailAdminModelForm):

    def clean(self):
        cleaned_data = super().clean()

        # Check scheduled publishing fields.
        go_live_at = cleaned_data.get('go_live_at')
        expire_at = cleaned_data.get('expire_at')
        if go_live_at and expire_at:
            # go_live_at must be before expire_at.
            if go_live_at > expire_at:
                msg = 'If set, Go live date/time must be before Expiry date/time'
                self.add_error('go_live_at', forms.ValidationError(msg))
                self.add_error('expire_at', forms.ValidationError(msg))

        # expire_at must be in the future.
        if expire_at and expire_at < timezone.now():
            self.add_error('expire_at', forms.ValidationError('Expiry date/time must be blank or in the future'))

        # Don't allow an existing first_published_at to be unset by clearing the field
        if 'first_published_at' in cleaned_data and not cleaned_data['first_published_at']:
            del cleaned_data['first_published_at']

        return cleaned_data


class GalleryPhoto(ClusterableModel):
    """
    GalleryPhotos represent CaltechImages with additional info that lets us place them into PhotoGalleryPopupBlocks in
    a customized manner.
    """

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='+'
    )
    live = models.BooleanField(
        verbose_name='Is Live',
        default=False,
        help_text='IMPORTANT: This item will not appear (even if you set "Go-live date/time") unless this checkbox is '
                  'checked. This is to help prevent you from releasing it to the world before you are ready.'
    )
    go_live_at = models.DateTimeField(
        verbose_name='Go-live date/time',
        blank=True,
        null=True,
        help_text="If set, this item will not go live until this date (assuming 'Is Live' is set)."
    )
    expire_at = models.DateTimeField(
        verbose_name='Expiry date/time',
        blank=True,
        null=True,
        help_text='If set, this item will stop being displayed after this date.'
    )
    first_published_at = models.DateTimeField(
        verbose_name='First published at',
        blank=True,
        null=True,
        db_index=True,
        help_text="This field should rarely be touched. It will auto-populate the first time this item is saved with"
                  "the 'Is Live' checkbox checked. It's only editable to allow Admins to change this item's sort order."
    )
    last_published_at = models.DateTimeField(
        verbose_name='Last published at',
        null=True,
        editable=False
    )

    content_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('image'),
                FieldPanel('live'),
            ],
            heading='Gallery Photo'
        ),
    ]

    publishing_panels = [
        PublishingPanel(),
        MultiFieldPanel(
            [
                FieldPanel('first_published_at'),
            ],
            heading='Sorting and Display'
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(publishing_panels, heading='Publishing'),
        ],
        base_form_class=GalleryPhotoForm
    )

    class Meta:
        verbose_name = 'Gallery Photo'
        verbose_name_plural = 'Gallery Photos'
        ordering = ['-first_published_at']

    def __str__(self):
        """
        This value is shown at the top of the edit form for GalleryPhotos.
        """
        return f'Gallery Photo for {str(self.image)}'

    def __repr__(self):
        return f'<GalleryPhoto: photo_id={self.image.pk}, live={self.live}>'

    def save(self, **kwargs):
        # Set default value for created_at to now.
        # We cannot use auto_now_add as that will override any value that is set before saving.

        if self.live:
            now = timezone.now()
            self.last_published_at = now

            if self.first_published_at is None:
                self.first_published_at = now

        super().save(**kwargs)


class SimplePhoto(ClusterableModel):
    """
    An even simpler model to see what is the minimum set up to trigger: 'NoneType' object has no attribute '_meta'
    """

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='+'
    )
    live = models.BooleanField(
        verbose_name='Is Live',
        default=False,
    )

    content_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('image'),
                FieldPanel('live'),
            ],
            heading= 'Simple Photo'
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
        ],
    )

    class Meta:
        verbose_name = 'Simple Photo'
        verbose_name_plural = 'Simple Photos'


class RelatedLink(ClusterableModel):
    """
    And this happens with page choosers too
    """

    title = models.CharField(
        max_length=256,
    )
    link = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name='+'
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                PageChooserPanel('link'),
            ],
            heading= 'Related Link'
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
        ],
    )

    class Meta:
        verbose_name = 'Related Link'
        verbose_name_plural = 'Related Link'


class SimpleThing(ClusterableModel):
    """
    OK without choosers?
    """

    title = models.CharField(
        max_length=256,
    )
    live = models.BooleanField(
        verbose_name='Is Live',
        default=False,
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('live'),
            ],
            heading= 'Simple Thing'
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
        ],
    )

    class Meta:
        verbose_name = 'Simple Thing'
        verbose_name_plural = 'Simple Thing'


class RelatedDocument(ClusterableModel):
    """
    All choosers broken?
    """

    title = models.CharField(
        max_length=256,
    )
    doc = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        DocumentChooserPanel('doc'),
    ]

    # content_panels = [
    #     MultiFieldPanel(
    #         [
    #             FieldPanel('title'),
    #             DocumentChooserPanel('doc'),
    #         ],
    #         heading= 'Related Document'
    #     ),
    # ]

    # edit_handler = TabbedInterface(
    #     [
    #         ObjectList(content_panels, heading='Content'),
    #     ],
    # )

    class Meta:
        verbose_name = 'Related Document'
        verbose_name_plural = 'Related Documents'
