from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import GalleryPhoto

class GalleryPhotoAdmin(ModelAdmin):
    model = GalleryPhoto
    menu_label = "Gallery Photos"
    menu_icon = "fa-clone"
    menu_order = 126
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('image', 'live', 'first_published_at', 'display_location_names')
    search_fields = ('image__title', 'image__photo_credit', 'image__caption',)


modeladmin_register(GalleryPhotoAdmin)

