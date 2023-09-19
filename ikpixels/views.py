from django.shortcuts import (render,get_object_or_404,redirect)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from . forms import SubscriptionUploadForm
from django.shortcuts import render
from django.shortcuts import render

def ticket(request):
	context = {}
	return render(request,'ik/web.html')

def music(request):
	context = {}
	return render(request,'ik/music.html')


@login_required(login_url ="account:login")
@csrf_exempt
def upload_payments(request):
	context = {}
	form = SubscriptionUploadForm()
	context['form'] = form
	return render(request,'ik/upload_payment.html',context)

def upload_payments(request):
	context = {}
	return render(request,'ik/upload_payment.html')

def upload_payments(request):
	context = {}
	return render(request,'ik/upload_payment.html')
