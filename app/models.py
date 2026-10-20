from PIL import Image
from django.db import models
# import os
# from django.utils import timezone
# from django.contrib.auth.models import User

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    class Meta:
        db_table = "artist"

    def __str__(self):
        return f"{self.id} {self.name}"

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    cover_image = models.ImageField(
        upload_to="album_covers/",
        default="album_covers/album-placeholder.png",
        null=True,
        blank=True
    )
    release_year = models.IntegerField()
    GENRE_CHOICES = [
        ('blues', 'Blues'),
        ('classical', 'Classical'),
        ('country', 'Country'),
        ('jazz', 'Jazz'),
        ('other', 'Other'),
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('r&B', 'R&B'),
    ]
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default='other'
    )
    producer_name = models.CharField(
        max_length=30
    )
    record_label = models.CharField(
        max_length=30
    )
    comment = models.TextField(
        max_length=600,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "album"

    def __str__(self):
        return f"{self.title} {self.artist.name} {self.release_year}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_path = self.cover_image.path
        if self.cover_image:
            img = Image.open(self.cover_image.path)

        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(img_path)

