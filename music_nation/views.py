
from django.shortcuts import (render,get_object_or_404,redirect)


from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect

from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages

from .forms import SignUpForm,CustomerForm,PaymentForm
from .models import Album, Song, Customer, Podcasts,contacts,Album_comments
from .forms import NewAlbum, NewSong

from Store.models import Product,Orders
from Event.models import Ticket
from music_nation import snipt
#from Store.views import cart_snipt
from ikpixels.models import MusicorEventPayment,PymtCode

import authorize

##########################################################
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def default_music_playlist(request,context):
    context['player_song'] = Song.objects.all()

def playlist_snipt(request,context):
    #for playlist counter, fetching song ids added by user from cookies
    if 'song_ids' in request.COOKIES:
        song_ids = request.COOKIES['song_ids']
        counter=song_ids.split('|')
        song_count_in_playlist=len(set(counter))
    else:
        song_count_in_playlist = 0
    context['song_count_in_playlist'] = song_count_in_playlist

    context['home_song'] = Song.objects.all().last()
    context['song'] = Song.objects.all()[:6]

def home(request):

    context = {}

    playlist_snipt(request,context)
    default_music_playlist(request,context)

    #show all albums in chronological order of it's upload
    albums = Album.objects.all()[:10]
    context['albums'] = albums
    context['song'] = Song.objects.all().last()
    context['top_10'] = Song.objects.all().order_by('-streamingCount')[
    :10]
    context['top_album'] =  Album.objects.all().order_by('-streamNum')[:10]
    context['events'] = Ticket.ticketObjects.all()
    context['products']= Product.objects.all()
    context['Artist'] = Customer.objects.filter(account_type="Artist")
    all_songs = Song.objects.all()[:10]
    context['all_songs'] = all_songs
    context['video'] = Podcasts.objects.all().order_by('-id')
  
    return render(request, 'www/index.html',context)
#........................................................#


def allTrack(request):
    context = {}

    default_music_playlist(request,context)
    playlist_snipt(request,context)

    tracks = Song.objects.all()

    query =request.GET.get('q')
    context['q_name'] = "Album name,genre"

    if query:
        context['search_title'] = query
        tracks =tracks.filter(Q(song_name__icontains=query)|
                              Q(Artist__icontains=query)).distinct().order_by('-id')

    '''page = request.GET.get('page', 1)
    paginator = Paginator(tracks,12)

    try:
        tracks = paginator.page(page)
    except PageNotAnInteger:
        tracks = paginator.page(1)
    except EmptyPage:
        tracks = paginator.page(paginator.num_pages)'''

    context['tracks'] = tracks
    context['events'] = Ticket.ticketObjects.all()
    context['products']= Product.objects.all()
    context['albums'] = Album.objects.all()[:5]
    context['songs'] = Song.objects.all()#buy model


    if is_ajax(request) and request.GET.get('data_'):
        cate = request.GET.get('data_')
        context['tracks'] =  Song.objects.filter(song_genre=str(cate))
        html = render_to_string('www/music2.html',context)
        return JsonResponse({'data':html})

    if is_ajax(request) and request.GET.get('song_id'):
        download_counts = Song.objects.get(id=request.GET['song_id'])
        download_counts.downloads += 1
        download_counts.save()
       

    return render(request, 'www/music.html',context)

@csrf_exempt
def Contacts(request):
    context = {}

    default_music_playlist(request,context)
    playlist_snipt(request,context)

    if is_ajax(request):
        email = request.GET.get('email')
        name=request.GET.get('name')
        subject =request.GET.get('subject')
        body =request.GET.get('text')
        form=contacts(name=name,email=email,subject=subject,body=body)
        form.save()
       
    return render(request, 'www/contacts.html',context)
   

#........................................................#

def Artist(request):
    context = {}

    if is_ajax(request) and request.GET.get('data'): #Adding number of streaming to song and album models
        id_ = request.GET.get('data')
        song_ = Song.objects.get(id=id_)
        song_.streamingCount += 1 #song
        album_ = Album.objects.get(id=song_.song_album.id)
        album_.streamNum += 1 #Album
        album_.save()
        song_.save()

    default_music_playlist(request,context)
    playlist_snipt(request,context)

    context['events'] = Ticket.ticketObjects.all()
   
    Artist = Customer.objects.filter(account_type="Artist")

    query =request.GET.get('q')

    context['q_name'] = "Artist name"
    if query:
        context['search_title'] = query
        Artist =Artist.filter(Q(user__icontains=query)).distinct().order_by('-id')

    #page = request.GET.get('page', 1)
    #paginator = Paginator(Artist,12)

    '''try:
        Artist = paginator.page(page)
    except PageNotAnInteger:
        Artist = paginator.page(1)
    except EmptyPage:
        Artist = paginator.page(paginator.num_pages)'''
    context ['Artist'] = Artist

    if is_ajax(request) and request.GET.get('artists_data'):
        context['Artist'] = Customer.objects.filter(artist_genre=request.GET.get('artists_data'))[:12]
        html = render_to_string('www/artists2.html',context)
        return JsonResponse({'data':html})


    return render(request, 'www/artists.html',context)

#........................................................#

def ArtistDetail(request,slug):
    context = {}

    playlist_snipt(request,context)
    default_music_playlist(request,context)

    Artist = Customer.objects.get(slug=slug)
    context['Artist'] = Artist

    albums = Album.objects.filter(album_artist=Artist.user)
    context['albums'] = albums
    context['musichead'] = "Releases by " + str(Artist)

    context['events'] = Ticket.ticketObjects.all()

    
    return render(request, 'www/artist.html',context)


#........................................................#
@csrf_exempt
def allMusic(request):
    context = {}

    default_music_playlist(request,context)
    playlist_snipt(request,context)

    albums = Album.objects.all()
    
    
    query =request.GET.get('q')
    context['q_name'] = "Album name,genre"

    if query:
        context['search_title'] = query
        albums =albums.filter(Q(album_name__icontains=query)|
                          Q(album_genre__icontains=query)).distinct().order_by('-id')

    '''page = request.GET.get('page', 1)
    paginator = Paginator(albums,12)

    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)'''

    context['albums'] = albums
    context['events'] = Ticket.ticketObjects.all()
    context['products']= Product.objects.all()


    if is_ajax(request):
        cate = request.GET['data']
        context['albums'] =  Album.objects.filter(album_genre=str(cate))
        html = render_to_string('www/releases2.html',context)
        return JsonResponse({'data':html})

    return render(request, 'www/releases.html',context)

#........................................................#
@csrf_exempt
def add_to_playlist(request,pk):

    context = {}

    song=Song.objects.all()
    albums = Album.objects.all()

    default_music_playlist(request,context)
    
    #for playlist counter, fetching song ids added by user from cookies
    if 'song_ids' in request.COOKIES:
        song_ids = request.COOKIES['song_ids']
        counter=song_ids.split('|')
        song_count_in_playlist=len(set(counter))
    else:
        song_count_in_playlist =1

    response = render(request, 'www/releases.html',{'albums':albums,'songs':song,'song_count_in_playlist':song_count_in_playlist})

    #adding product id to cookies
    if 'song_ids' in request.COOKIES:
        song_ids = request.COOKIES['song_ids']
        if song_ids=="":
            song_ids=str(pk)
        else:
            song_ids=song_ids+"|"+str(pk)
        response.set_cookie('song_ids', song_ids)
    else:
        response.set_cookie('song_ids', pk)

    song=Song.objects.get(id=pk)
    messages.info(request, song.song_name + ' added to cart successfully!')

    return response

#........................................................#
@csrf_exempt
def playlist_view(request):

    context = {}
    
    playlist_snipt(request,context)

    # fetching song details from db whose id is present in cookie
    song=None

    if 'song_ids' in request.COOKIES:
        song_ids = request.COOKIES['song_ids']
        if song_ids != "":
            song_id_in_cart= song_ids.split('|')
            song=Song.objects.all().filter(id__in = song_id_in_cart)
    context['song'] = song

    context['products'] = Product.objects.all()

    return render(request,'www/playlist.html',context)

#........................................................#
@csrf_exempt
def remove_from_playlist(request,pk):

    context = {}

    default_music_playlist(request,context)
    playlist_snipt(request,context)

    # removing song id from cookie
 
    if 'song_ids' in request.COOKIES:
        song_ids = request.COOKIES['song_ids']
        song_id_in_playlist=song_ids.split('|')
        song_id_in_playlist=list(set(song_id_in_playlist))
        song_id_in_playlist.remove(str(pk))
        song=Song.objects.all().filter(id__in = song_id_in_playlist)
        #for total price shown in cart after removing product
        
        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(song_id_in_playlist)):
            if i==0:
                value=value+song_id_in_playlist[0]
            else:
                value=value+"|"+song_id_in_playlist[i]
        context['song'] =song
        response = render(request, 'www/playlist.html',context)
        if value=="":
            response.delete_cookie('song_ids')
        response.set_cookie('song_ids',value)
        return response

#........................................................#

def about(request):
    context = {}
    default_music_playlist(request,context)
    return render(request, 'www/about.html',context)
#........................................................#
@login_required(login_url ="account:login")
@csrf_exempt
def updateCustomer(request,id):
    context = {}

    default_music_playlist(request,context)
    playlist_snipt(request,context)
    Artist = Customer.objects.get(id=id)

    customerForm = CustomerForm(instance=Artist)
    context['form'] = customerForm

    if request.method == "POST":
        customerForm = CustomerForm(request.POST,request.FILES, instance=Artist)
        if customerForm.is_valid():
            customerForm.save()
            return redirect('music_nation:ArtistDetail', slug=Artist.slug)

    return render(request, 'www/updateCustomer.html',context)

#........................................................#

@login_required(login_url ="account:login")
def profile_detail(request, username):

    context = {}
    # show all albums of the artist

    default_music_playlist(request,context)

    albums = get_object_or_404(User, username=username)
    albums = albums.albums.all()

    context['albums'] = albums
    context['username'] = username

    return render(request, 'www/useralbum-list.html',context)

#........................................................#

@login_required(login_url ="account:login")
@csrf_exempt
def add_album(request, username):

    context = {}
    default_music_playlist(request,context)


    try:
        Subscription = PymtCode.objects.filter(active=True,customer=str(request.user),Mid='MUC').last()
        if Subscription:
            pass
        else:
            return redirect('ikpixels:upload_payment')
    except PymtCode.DoesNotExist:
        return redirect('ikpixels:upload_payment')

    user = get_object_or_404(User, username=username)
    #only currently logged in user can add album else will be redirected to home
    if user == request.user:
        if request.method == 'POST':
            form = NewAlbum(request.POST, request.FILES)
            if form.is_valid():
                # form.save(commit='False')
                album = Album.objects.create(
                    album_logo=form.cleaned_data.get('album_logo'),
                    album_name=form.cleaned_data.get('album_name'),
                    album_genre=form.cleaned_data.get('album_genre'),
                    sell=form.cleaned_data.get('sell'),
                    price =form.cleaned_data.get('price'),
                    uploaded_on = timezone.now(),
                    album_artist = request.user
                )
                return redirect('music_nation:profile_detail', username=request.user)
        else:
            form = NewAlbum()
            context['form'] = form
        return render(request, 'www/addAlbum.html',context)
    else:
        return redirect('music_nation:profile_detail', username=user)

#........................................................#
@csrf_exempt
def album_detail(request,slug):

    context = {}

    default_music_playlist(request,context)
    playlist_snipt(request,context)

    #show album details here. single album's details.
    album = get_object_or_404(Album, slug=slug)
    songs = get_object_or_404(User, username=album.album_artist)
    songs = songs.albums.get(album_name=str(album))
    songs = songs.songs.all()

    context['songs'] = songs
    context['album'] = album
    context['username'] = album.album_artist
    context['msg_count'] = Album_comments.objects.all().count()
    context['msg'] = Album_comments.objects.filter(album=album).order_by('-id')[:12]

    if is_ajax(request):
        msg = Album_comments(
            body = request.GET.get('text'),
            user = request.user,album = album)
        msg.save()
        context['msg_count'] = Album_comments.objects.filter(album=album).count()
        context['msg'] = Album_comments.objects.filter(album=album).order_by('-id')[:12]
        html = render_to_string('www/music_msg.html',context)
        return JsonResponse({'data':html})


    #context['other_releases'] = Album.objects.exclude(album_name=album)[:6]

    return render(request, 'www/release.html',context)


#........................................................#

@login_required(login_url ="account:login")
@csrf_exempt
def add_song(request,id):

    context = {}



    default_music_playlist(request,context)

    try:
        Subscription = PymtCode.objects.filter(active=True,customer=str(request.user),Mid='MUC').last()
        if Subscription:
            pass
        else:
            return redirect('ikpixels:upload_payment')
    except PymtCode.DoesNotExist:
        return redirect('ikpixels:upload_payment')

    user = get_object_or_404(User, username=request.user)

    if request.user == user:

        album_get = Album.objects.get(id=id)

        if request.method == 'POST':
            form = NewSong(request.POST, request.FILES)
            if form.is_valid():
                song = Song.objects.create(
                    song_name = form.cleaned_data.get('song_name'),
                    Artist =form.cleaned_data.get('Artist'),
                    year =form.cleaned_data.get('year'),
                    song_file = form.cleaned_data.get('song_file'),
                    sell = form.cleaned_data.get('sell'),
                    price = form.cleaned_data.get('price'),
                    song_genre = form.cleaned_data.get('song_genre'),
                    artwork = form.cleaned_data.get('artwork'),
                    song_album = album_get
                )
                album_get.songsNum += 1
                album_get.save()
                Subscription.active=False
                Subscription.save()
                return redirect('music_nation:album_detail', slug=album_get.slug)

        else:
            form = NewSong()
            context['form'] = form
            return render(request, 'www/add_new_song.html',context)
    else:
        return redirect('music_nation:album_detail', slug=album_get.slug)


@csrf_exempt
def podcasts(request):

    context = {}

    playlist_snipt(request,context)
    default_music_playlist(request,context)

    podcasts = Podcasts.objects.all().order_by('-id')

    query =request.GET.get('q')
    context['q_name'] = "Podcast title"

    if query:
        context['search_title'] = query
        podcasts =podcasts.filter(Q(title__icontains=query)).distinct().order_by('-id')

    '''page = request.GET.get('page', 1)
    paginator = Paginator(podcasts,12)

    try:
        podcasts = paginator.page(page)
    except PageNotAnInteger:
        podcasts = paginator.page(1)
    except EmptyPage:
        podcasts = paginator.page(paginator.num_pages)'''

    context['podcasts'] = podcasts

    context['events'] = Ticket.ticketObjects.all()
    context['products']= Product.objects.all()
  
    if is_ajax(request) and request.GET.get('data'):
       id_ = request.GET.get('data')
       pod = Podcasts.objects.get(id=id_)
       pod.views += 1
       pod.save()

    if is_ajax(request) and request.GET.get('podcast_id'):
        context['podcasts'] = Podcasts.objects.filter(category=request.GET.get('podcast_id'))[:12]
        html = render_to_string('www/podcasts2.html',context)
        return JsonResponse({'data':html})

    return render(request, 'www/podcasts.html',context)