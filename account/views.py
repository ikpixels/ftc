from django.shortcuts import render,redirect
from Store.models import Product
from Event.models import tickets_order,Ticket
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from music_nation.forms import SignUpForm,CustomerForm
from music_nation.models import Album, Song, Customer, Podcasts
from music_nation.forms import NewAlbum, NewSong
from music_nation.views import playlist_snipt,default_music_playlist
from music_nation.forms import PodcastForm
from Store.views import cart_snipt
from Store.models import Product,Orders
from Event.models import Ticket
from ikpixels.models import MusicorEventPayment

# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def error_404(request,exception):
    context = {}
    context['error'] = exception
    return render(request,'account/404.html',context)

def error_500(request):
    context = {}
    return render(request,'account/500.html',context)

@csrf_exempt
def signup(request):

    context = {}

    playlist_snipt(request,context)
    default_music_playlist(request,context)
    cart_snipt(request,context)
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if form.is_valid() and customerForm.is_valid():
            user = form.save()

            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            
            login(request, user)
            return redirect('account:profile')
        else:
            message = 'Looks like a username with that email or password already exists'
            context['message'] = message
            context['customerForm'] = customerForm
            context['form'] = form
            return render(request, 'account/signup.html',context)
    else:
        form = SignUpForm()
        customerForm=CustomerForm()
        context['customerForm'] = customerForm
        context['form'] = form
        return render(request, 'account/signup.html',context)

#........................................................#
@csrf_exempt
def login_view(request):
    context = {}

    playlist_snipt(request,context)
    default_music_playlist(request,context)
    cart_snipt(request,context)

    if request.method =="POST":
        username = request.POST['name']
        password = request.POST['pass']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            if user.is_superuser:
                return redirect('account:profile')
            else:
                return redirect('account:profile')
        else:
            context['error']="Provide valide Credientials!!!"
    return render(request,"account/signin.html",context)

@login_required(login_url ="account:login")
@csrf_exempt
def profile(request):
    context = {}

    playlist_snipt(request,context)
    default_music_playlist(request,context)
    cart_snipt(request,context)

    Form = PodcastForm()
    if request.method == 'POST':
        Form = PodcastForm(request.POST)
        Form = Form.save(commit=False)
        Form.user  = request.user
        Form.save()
        return redirect ('music_nation:podcasts')

    context['form'] = Form

    
    #adminlogin
    if request.user.is_superuser:

        customercount=Customer.objects.all().count()
        productcount=Product.objects.all().count()
        ordercount=Orders.objects.all().count()

        orders= Orders.objects.all()
        ordered_products=[]
        ordered_bys=[]

        for order in orders:
            ordered_product=Product.objects.all().filter(id=order.product.id)
            ordered_by= Customer.objects.all().filter(id = order.customer.id)
            ordered_products.append(ordered_product)
            ordered_bys.append(ordered_by)

        context['customercount'] = customercount
        context['productcount'] = productcount
        context['ordercount'] = ordercount
        context['data'] = zip(ordered_products,ordered_bys,orders)

        return render(request, 'www/admindashboard.html',context)

    else:#customerlogin

        customer= Customer.objects.get(user_id=request.user.id)
        orders=  Orders.objects.all().filter(customer_id = customer)
        ordered_products=[]
        for order in orders:
            ordered_product= Product.objects.all().filter(id=order.product.id)
            ordered_products.append(ordered_product)
            context['data'] = zip(ordered_products,orders)

        context['ArtistID']  = Customer.objects.get(user=request.user)
        context['podcount'] = Podcasts.objects.filter(user=request.user).count()
        context['musiccount'] = Album.objects.filter(album_artist=request.user).count()
        context['ticketcount'] = Ticket.ticketObjects.filter(client=request.user).count()
        context['Subscription'] = MusicorEventPayment.objects.filter(user=request.user).count()
        context['albums'] = Album.objects.all()
        return render(request, 'account/profile.html',context)
#........................................................#




#@login_required(login_url='account:adminlogin')

#@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url ="account:login")
def truck_ticket_order(request):

    context = {}
    playlist_snipt(request,context)
    default_music_playlist(request,context)
    cart_snipt(request,context)
    context['q_name'] = "Search order"

    if request.user.is_superuser:
        booked_ticket = Ticket.ticketObjects.filter(ticket_booked__gte = 1)
    else:
        booked_ticket = Ticket.ticketObjects.filter(ticket_booked__gte = 1,client=request.user)

    context['ticket'] = booked_ticket
    return render(request,'account/truck_ticket.html',context)

@user_passes_test(lambda u: u.is_superuser)
def adminAproveMusic(request):
    context = {}

    songs = Song.adminAprove.all().order_by('-id')[:12]

    context['q_name'] = "Search release"
    query =request.GET.get('q')

    if query:
        context['search_title'] = query
        songs =songs.filter(Q(Artist__icontains=query)|
                            Q(song_album__icontains=query)).distinct().order_by('-id')


    context['songs'] =  songs


    if is_ajax(request) and request.GET.get('data'):

        song = Song.adminAprove.get(id=request.GET.get('data'))

        # to avoid album query does does not exisit error if it aproved twice
        try:
            album_ = Album.AdminAlbumAproval.get(id=song.song_album.id)
            album_.aproved = True
            album_.save()
        except Album.DoesNotExist:
            pass 

        song.aproved = True
        song.save()

        songs_ = Song.adminAprove.all().order_by('-id')[:12]
        context['songs'] = songs_
        
        html = render_to_string('account/adminAproveMusic2.html',context)
        return JsonResponse({'data':html})
        
    

    return render(request,'account/adminAproveMusic.html',context)