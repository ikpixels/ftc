from django.shortcuts import (render,get_object_or_404,redirect)
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from . forms import SubscriptionUploadForm
from django.shortcuts import render
from django.shortcuts import render
from music_nation.views import playlist_snipt,default_music_playlist
from Store.views import cart_snipt
from . models import MusicorEventPayment,PymtCode
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from music_nation import snipt
from music_nation.models import Song

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ticket(request):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	return render(request,'ik/web.html')

def music(request):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	return render(request,'ik/music.html')


def pricing(request):
	context = {}
	return render(request,'ik/pricing.html')


@login_required(login_url ="account:login")
@csrf_exempt
def upload_payments(request,id=None,item=None):
	context = {}

	try:
		pymt = MusicorEventPayment.objects.filter(user=request.user,aprove=False)
		if pymt:
			msg = "Your payment approval  is still on pending..."
			context['warningColor'] = "red"
		else:
			msg = "Subsicribe first"
	except MusicorEventPayment.DoesNotExist:
		msg = "Subsicribe first"
	context['msg'] = msg

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)


	if item == "release":
		release = Song.objects.get(id=int(id))
		context['pymt_info'] = release
	else:
		pass

	context['form'] = SubscriptionUploadForm()
	if request.method == "POST":
		form = SubscriptionUploadForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = request.user
			if item == "release":
				form.item_id = release.id
			form.save()
			return redirect('ikpixels:payment_success')

	return render(request,'ik/upload_payment.html',context)


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def uprove_upload_pymt(request,id=None):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	payment = MusicorEventPayment.objects.filter(aprove=False)

	query =request.GET.get('q')
	context['q_name'] = "Search name, pymt method, trans type"

	if query:
		context['search_title'] = query
		payment =payment.filter(Q(payment_method__icontains=query)|
			                    Q(category__icontains=query)|
			                    Q(PaymentReferenceNumber__icontains=query)|
                                Q(name__icontains=query)).distinct().order_by('-id')

	context['payment']=payment


	if is_ajax(request) and request.GET.get('data'):

		pymt_aproved = MusicorEventPayment.objects.get(id=request.GET.get('data'))
		pymt_aproved.aprove = True

		if pymt_aproved.category == "Event":
			code = PymtCode(Mid='EUC',customer=pymt_aproved.user,codeValue=pymt_aproved.amount,code=snipt.secret_code(),codeOwner="admin")
			code.save()
		if pymt_aproved.category == "Music":
			code = PymtCode(Mid='MUC',customer=pymt_aproved.user,codeValue=pymt_aproved.amount,code=snipt.secret_code(),codeOwner="admin")
			code.save()
		if pymt_aproved.category == "Music_Purchase":
			artist = Song.objects.get(id=int(pymt_aproved.item_id)).song_album.album_artist
			mid = "MDC"+'-'+ pymt_aproved.item_id
			code = PymtCode(Mid=mid,customer=pymt_aproved.user,codeValue=pymt_aproved.amount,code=snipt.secret_code(),codeOwner=artist)
			code.save()

		pymt_aproved.save()

		payment = MusicorEventPayment.objects.filter(aprove=False)
		context['payment'] = payment

		html = render_to_string('ik/pymt_list_2.html',context)
		return JsonResponse({'data':html})

	return render(request,'ik/pymt-list.html',context)


@login_required(login_url ="account:login")
def userMoney(request):
	context = {}
	code = PymtCode.objects.filter(codeOwner=request.user)
	context['money'] = code
	context['paid'] = PymtCode.objects.filter(codeOwner=request.user,paid=True).count()
	context['notPaid'] = PymtCode.objects.filter(codeOwner=request.user,paid=False).count()
	context['total'] = PymtCode.objects.filter(codeOwner=request.user).count()
	return render(request,'ik/money.html',context)


@login_required(login_url ="account:login")
def paymentDetail(request,user):
	context = {}

	playlist_snipt(request,context)
	default_music_playlist(request,context)
	cart_snipt(request,context)

	payment = MusicorEventPayment.objects.filter(user=request.user)
	query =request.GET.get('q')
	context['q_name'] = "Search subscription"

	if query:
		context['search_title'] = query
		payment =payment.filter(Q(name__icontains=query)|
        	                    Q(payment_method__icontains=query)|
        	                    Q(category__icontains=query)|
        	                    Q(PaymentReferenceNumber__icontains=query)|
        	                    Q(aprove__icontains=query)|
                                Q(created_at__icontains=query)).distinct().order_by('-id')

	context['payment'] = payment
	return render(request,'ik/pymtDetail.html',context)

