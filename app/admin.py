from django.contrib import admin
from .models import Album, Artist

# Register your models here.

# admin.site.register(Album)
# admin.site.register(Artist)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_year')
    ordering = ('title',)
    search_fields  = ('title', 'artist')

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)
    search_fields  = ('id', 'name')


# admin.site.register(Album, AlbumAdmin)
# admin.site.register(Artist, ArtistAdmin)