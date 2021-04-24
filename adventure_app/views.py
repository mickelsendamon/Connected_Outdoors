from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *


def login_page(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/adventures')
        messages.error(request, "Email or password are wrong!")
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def register(request):
    return render(request, "register.html")


def registration(request):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()

            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
            request.session['user_id'] = user.id
            return redirect('/adventures')
    return redirect('/')


def adventures_page(request):
    return render(request, "adventures.html")


def join_adventure(request):
    return redirect('adventures')


def leave_adventure(request):
    return redirect('adventures')


def my_adventures(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, "my_adventures.html", context)


def adventure_detail(request, adv_id):
    return render(request, "adventure_details.html")


def cancel_adventure(request, adv_id):
    return redirect('adventures')


def new_adventure(request):
    return render(request, "new_adventure.html")


def create_adventure(request):
    return redirect('adventures')
