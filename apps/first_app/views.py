from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
import re
import datetime
import pytz
from .models import User, Quote

# Create your views here.
def index(request):
    if 'logged_in' not in request.session.keys():
        request.session['logged_in'] = False
        print request.session['logged_in']
        return render(request, "first_app/index.html")
    if request.session['logged_in'] == False:
        return render(request, "first_app/index.html")
        print request.session['logged_in']
    else:
        print request.session['logged_in']
        return redirect('/display_quotes')

def process_registration(request):
    if request.method == "POST":
        error = False
         # for now i am passing in the entire request object for the sake of the django messages(will fix), and i am using session to repopulate the fields,
        user = User.objects.register(request.POST, request.session, request)
        error = False
        if user:
            return redirect('/display_quotes')
        return redirect('/')
    return redirect('/')

def process_login(request):
    if request.method == "POST":
        error = False
        # for now i am passing in the entire request object for the sake of the django messages(will fix), and i am using session to repopulate the fields
        user = User.objects.login(request.POST, request.session, request)
        if user:
            return redirect('/display_quotes')
        else:         
            return redirect('/login')
        return redirect('/login')

def login(request):
    return render(request, "first_app/login.html")

def log_out(request):
    request.session.pop('logged_in')
    return redirect('/login')

def display_quotes(request):
    try:
        if request.session['logged_in'] == False:
            return redirect('/')
            print request.session['logged_in']
    except:
        request.session['logged_in'] == False

    else:
        current_user = User.objects.get(email=request.session['logged_in'])

        context = {
        "current_user": current_user,
        "not_fav_quotes": Quote.objects.all().exclude(users__id=current_user.id),
        }
        return render(request, 'first_app/display_quotes.html', context)
    

def process_quote(request):
    if request.method == "POST":
        error = False
        author = request.POST['author']
        quote = request.POST['quote']
        if len(author) < 3:
            messages.error(request, 'Author must have at least 3 characters!') 
            error = True
        if len(quote) < 10:
            messages.error(request, 'Quote must have at least 10 characters!') 
            error = True
        if error == True:
            return redirect(reverse('first_app:display_quotes'))
        else:
            user = User.objects.get(email=request.session['logged_in'])
            print user
            new_quote= Quote.objects.create(author = author, quote = quote, posted_by = user)
            return redirect(reverse('first_app:display_quotes'))    

    return redirect('/')

    
def add_fav(request, id):
    if request.method == "POST":
        user = User.objects.get(email=request.session['logged_in'])
        fav_quote = Quote.objects.get(id=id)
        fav_quote.users.add(user)
        fav_quote.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

def remove_fav(request, id):
    if request.method == "POST":
        user = User.objects.get(email=request.session['logged_in'])
        quote = Quote.objects.get(id=id)
        removed = quote.users.remove(user)
        print removed
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

def delete_quote(request, id):
    if request.method == "POST":
        quote = Quote.objects.get(id=id)
        print quote
        quote.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('/')


def display_user(request, id):
    current_user = User.objects.get(email=request.session['logged_in'])
    context = {
        "current_user": current_user,
        "user": User.objects.get(id = id),
    }
    return render(request, 'first_app/display_user.html', context) 