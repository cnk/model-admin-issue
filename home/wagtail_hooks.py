from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import GalleryPhoto, SimplePhoto, SimpleThing, RelatedLink, RelatedDocument

class GalleryPhotoAdmin(ModelAdmin):
    model = GalleryPhoto
    menu_label = "Gallery Photos"
    menu_order = 126
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('image', 'live', 'first_published_at')
    search_fields = ('image__title',)


modeladmin_register(GalleryPhotoAdmin)

class SimplePhotoAdmin(ModelAdmin):
    model = SimplePhoto
    menu_label = "Simple Photos"
    menu_order = 130
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('image', 'live')
    search_fields = ('image__title',)


modeladmin_register(SimplePhotoAdmin)


class SimpleThingAdmin(ModelAdmin):
    model = SimpleThing
    menu_label = "Simple Things"
    menu_order = 135
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('title', 'live')
    search_fields = ('title',)


modeladmin_register(SimpleThingAdmin)


class RelatedLinkAdmin(ModelAdmin):
    model = RelatedLink
    menu_label = "Related Links"
    menu_order = 135
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('title', 'link')
    search_fields = ('title',)


modeladmin_register(RelatedLinkAdmin)


class RelatedDocumentAdmin(ModelAdmin):
    model = RelatedDocument
    menu_label = "Related Documents"
    menu_order = 137
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('title', 'link')
    search_fields = ('title',)


modeladmin_register(RelatedDocumentAdmin)

