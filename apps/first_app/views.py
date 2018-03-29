from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Q
from models import *
import bcrypt

def index(request):
    return render(request, 'first_app/loginreg.html')

def success(request):
    if 'id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'quotable': Quote.objects.all()
        }
    # errors = Quote.objects.quote_validator(request.POST)
    # if len(errors):
    #     for tag, error in errors.iteritems():
    #         messages.error(request, error, extra_tags=tag)
    #     return redirect('/success')
    return render(request, 'first_app/wall.html', context)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error, extra_tags=tag)
        return redirect('/')
    hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    print hash1
    session = User.objects.create(firstname=request.POST["firstname"], lastname=request.POST["lastname"],
    email=request.POST["email"], password=hash1)
    request.session['id'] = session.id
    return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    email = request.POST['email']
    request.session['id'] = User.objects.get(email=email).id
    return redirect('/success')

def logout(request):
    request.session.clear() 
    return redirect('/')


def createitem(request):
    Quote.objects.create(itemname=request.POST["itemname"], creator=User.objects.get(id= request.session['id']))
    return redirect('/success')

def home(request):
    return redirect('/success')

def userinfo(request):
  context = {
            'user': User.objects.get(id=request.session['id'])
        }
  return render(request, 'first_app/userinfo.html', context)