from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Album, Artist
from .forms import AlbumForm, ArtistForm

def home(request):
    return render(request, "homepage.html")

def auth(request):
    return render(request, "login.html")

def auth_status(request):
    return render(request, "admin/status.html")

def album_details(request, album_id):
    print(f'[DEBUG] album_details: ${album_id}')
    album = get_object_or_404(Album, id=album_id)
    return render(request, "albums/view_album_details.html", {"album": album})

def artist_details(request, artist_id):
    print(f'[DEBUG] artist_details: ${artist_id}')
    artist = get_object_or_404(Artist, id=artist_id)
    albums = Album.objects.filter(artist_id=artist_id)
    return render(request, "artists/view_artist_details.html", {"artist": artist, "albums": albums})

def display_albums(request):
    items = Album.objects.all()

    # Search filter
    search_query = request.GET.get('q', '')
    if search_query:
        items = items.filter(
            title__icontains=search_query
        ) | items.filter(
            artist__name__icontains=search_query
        ) | items.filter(
            genre__icontains=search_query
        )

    title = "Albums"
    return render(request, "albums/list_albums.html", {
        "album_list": items,
        "page_title": title,
        "search_query": search_query
    })

def display_artists(request):
    print('[DEBUG] all_artists')
    items = Artist.objects.all()

    # Search filter
    search_query = request.GET.get('q', '')
    if search_query:
        items = items.filter(
            name__icontains=search_query
        ) | items.filter(
            country__icontains=search_query
        )

    title = "Artist"
    return render(request, "artists/list_artists.html", {
        "artist_list": items,
        "page_title": title,
        "search_query": search_query
    })

@login_required
def add_album(request):
    submitted = False

    # handle POST
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add-album?submitted=True')

    else:
        # GET request
        initial_data = {}

        artist_id = request.GET.get("artist")
        if artist_id:
            initial_data["artist"] = artist_id

        form = AlbumForm(initial=initial_data)

        if 'submitted' in request.GET:
            submitted = True

    return render(request, "albums/add_album.html", {
        "form": form,
        "submitted": submitted
    })


@login_required
def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('album-details', album_id=album.id)
    else:
        form = AlbumForm(instance=album)

    return render(request, "albums/edit_album.html", {'form': form, 'album': album})


@login_required
def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == "POST":
        album.delete()
        return redirect('albums')

    return render(request, "albums/delete_album.html", {'album': album})


@login_required
def add_artist(request):
    submitted = False
    if request.method == "POST":
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add-artist?submitted=True')
    else:
        form = ArtistForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, "artists/add_artist.html", {'form': form, 'submitted': submitted})


@login_required
def edit_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    if request.method == "POST":
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('artist-details', artist_id=artist.id)
    else:
        form = ArtistForm(instance=artist)

    return render(request, "artists/edit_artist.html", {'form': form, 'artist': artist})


@login_required
def delete_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    linked_albums = Album.objects.filter(artist_id=artist_id).count()

    if request.method == "POST":
        if linked_albums == 0:
            artist.delete()
            return redirect('artists')

    return render(request, "artists/delete_artist.html", {'artist': artist, 'linked_albums': linked_albums})