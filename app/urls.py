from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="homepage"),
    path("homepage/", views.home, name="homepage"),
    path("artist/", views.display_artists, name="artists"),
    path("artist/<int:artist_id>/", views.artist_details, name="artist-details"),
    path("artist/<int:artist_id>/edit/", views.edit_artist, name="edit-artist"),
    path("artist/<int:artist_id>/delete/", views.delete_artist, name="delete-artist"),
    path("albums/", views.display_albums, name="albums"),
    path("albums/<int:album_id>/", views.album_details, name="album-details"),
    path("albums/<int:album_id>/edit/", views.edit_album, name="edit-album"),
    path("albums/<int:album_id>/delete/", views.delete_album, name="delete-album"),
    path("add-album/", views.add_album, name="add-album"),
    path("add-artist/", views.add_artist, name="add-artist"),
]

