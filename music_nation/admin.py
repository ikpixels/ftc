from django.contrib import admin
from .models import Album, Song, Customer,Podcasts,contacts,Card_Payment,Album_comments
# Register your models here.

admin.site.register(Album)
admin.site.register(Customer)
admin.site.register(Podcasts)
admin.site.register(Card_Payment)
admin.site.register(Album_comments)


class SongAdmin(admin.ModelAdmin):
  list_display = ('song_name', 'Artist','streamingCount','downloads')
  list_per_page=12
  search_fields=['song_name','Artist','song_album__album_name',]

admin.site.register(Song,SongAdmin)


class ContactAdmin(admin.ModelAdmin):
  list_display = ('name', 'body',)
  list_per_page=12
  search_fields=['name','created_at',]

admin.site.register(contacts,ContactAdmin)