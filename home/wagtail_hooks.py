from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import GalleryPhoto

class GalleryPhotoAdmin(ModelAdmin):
    model = GalleryPhoto
    menu_label = "Gallery Photos"
    menu_order = 126
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('image', 'live', 'first_published_at')
    search_fields = ('image__title',)


modeladmin_register(GalleryPhotoAdmin)

