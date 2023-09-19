from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from qr_code.qrcode.utils import QRCodeOptions
from django.views.decorators.csrf import csrf_exempt
from . models import ticketsCategory
from music_nation.models import Customer
from music_nation.views import playlist_snipt,default_music_playlist
from Store.views import cart_snipt
from . models import tickets_order,Ticket
from Store.models import Product
from music_nation import snipt

from ikpixels.models import MusicorEventPayment,PymtCode

from . forms import EventForm,EventForm2


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def events(request):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	context['category'] = ticketsCategory.objects.all()

	events = Ticket.ticketObjects.all()

	query =request.GET.get('q')
	context['q_name'] = "Event title,venue"

	if query:
		context['search_title'] = query
		events =events.filter(Q(name__icontains=query)|Q(venue__icontains=query)).distinct().order_by('-id')

	'''page = request.GET.get('page', 1)
	paginator = Paginator(events,12)

	try:
		events = paginator.page(page)
	except PageNotAnInteger:
		events = paginator.page(1)
	except EmptyPage:
		events = paginator.page(paginator.num_pages)'''

	context['events'] = events

	if is_ajax(request) and request.GET.get('event_id'):
		context['events']=Ticket.ticketObjects.filter(ticketCategory=request.GET.get('event_id'))[:12]
		html = render_to_string('Event/events2.html',context)
		return JsonResponse({'data':html})

	return render(request,'Event/events.html',context)

def event_detail(request,id):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	event = Ticket.ticketObjects.get(id=id)
	context['event'] = event

	context['events'] = Ticket.ticketObjects.all()

	return render(request,'Event/event.html',context)


@login_required(login_url ="account:login")
@csrf_exempt
def ticket_order(request,id):

	context = {}

	context['q_name'] = "Search order"

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	if request.method == "POST":

		ticket_id = Ticket.ticketObjects.get(id=id)

		amount = request.POST['ticket_type']
		ref = request.POST['ref']
		p_method = request.POST['method']
		acc_name = request.POST['acc_name']
		acc_num = request.POST['acc_num']

		ticket = tickets_order.objects.create(user=request.user,
			                                  ticket=ticket_id,
			                                  ticket_type=amount,
			                                  ref=ref,
			                                  payment_mathod=p_method,
			                                  account_num=acc_num)
		ticket.save()

		ticket_id.ticket_booked += 1
		ticket_id.number_of_tickets -= 1
		ticket_id.save()

	return render(request,'Event/success.html',context)


@login_required(login_url ="account:login")
@csrf_exempt
def customer_event_booked(request):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	event = tickets_order.objects.filter(user=request.user).order_by('-updated_at')
	context['event'] = event

	context['my_options']=QRCodeOptions(size='t', border=6, error_correction='L')
	
	return render(request,'Event/customer_event_booked.html',context)

@login_required(login_url ="account:login")
@csrf_exempt
def add_event(request):
	context = {}

	try:
		Subscription = PymtCode.objects.get(customer=request.user).code
	except PymtCode.DoesNotExist:
		return redirect('ikpixels:upload_payment')

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	if request.method=='POST':
		form = EventForm(request.POST, request.FILES)
		if form.is_valid():
			form = form.save(commit=False)
			form.client = request.user
			form.save()
			return redirect('Event:events')
	else:
		form = EventForm()
		

	context['form'] = form
	return render(request,'Event/event_terms.html',context)

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_aprove_ticket(request):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	event = Ticket.Object.all()
	context['event'] = event
	return render(request,'Event/admin_event.html',context)


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_event_detail(request,id):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	event = Ticket.Object.get(id=id)
	context['event'] = event

	context['events'] = Ticket.ticketObjects.all()

	
	if request.method == "POST":
		Form = EventForm2(request.POST,request.FILES, instance=event)
		if Form.is_valid():
			Form = Form.save(commit=False)
			Form.ticket = True
			Form.save()
			return redirect('Event:admin_aprove_ticket')

	else:
		Form = EventForm2(instance=event)
	
	context['form'] = Form
	return render(request,'Event/admin_event_detail.html',context)


@login_required(login_url ="account:login")
@csrf_exempt
def approve_order(request,id):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	context['q_name'] = "Search order"

	ticket = Ticket.ticketObjects.get(id=id)
	context['event'] = ticket
	context['orders'] = tickets_order.objects.filter(ticket=ticket).order_by('-paid')


	if is_ajax(request):
		id_ = request.GET.get('data')

		order = tickets_order.objects.get(id=id_)
		code = snipt.secret_code()

		order.ticket_number = code
		order.paid = 'Approved'
		order.save()

		context['orders'] = tickets_order.objects.filter(ticket=ticket).order_by('-paid')
		html = render_to_string('Event/admin_approve_order2.html',context,request=request)
		return JsonResponse({'data':html})
	
	return render(request,'Event/admin_approve_order.html',context)
