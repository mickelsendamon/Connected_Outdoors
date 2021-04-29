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


def register_page(request):
    return render(request, "register.html")


def registration(request):
    if request.method == "POST":
        errors = User.objects.basic_validation(request.POST)
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
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_adventures': Adventure.objects.all().order_by('-adventure_start'),
        'all_sg_equipment': SuggestedEquipment.objects.all(),
        'all_activities': Activity.objects.all(),
    }
    return render(request, "adventures.html")


def join_adventure(request, adventure_id):
    if request.method == 'POST':
        if 'user_id' in request.session:
            this_adventure = Adventure.objects.get(id=adventure_id)
            this_adventure.participants.add(
                User.objects.get(id=request.session['user_id']))
        return redirect('/')
    return redirect('/adventures')


def leave_adventure(request, adv_id):
    if request.method == 'POST':
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            this_adventure = Adventure.objects.get(id=adv_id)
            this_adventure.participants.remove(user)
    return redirect('/adventures')


def my_adventures(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, "my_adventures.html", context)


def adventure_detail(request, adv_id):
    if request.method == 'POST':
        if 'user_id' in request.session:
            context = {
                'current_user': User.objects.get(id=request.session['user_id']),
                'current_adventure': Adventure.objects.get(id=adv_id),
            }
    return render(request, "adventure_details.html", context)


def cancel_adventure(request, adv_id):
    return redirect('adventures')


def new_adventure(request):
    if 'user_id' in request.session:
        context = {
            'all_activities': Activity.objects.all(),
            'all_equipments': SuggestedEquipment.objects.all(),

        }
        return render(request, "new_adventure.html", context)
    return redirect('/')


def create_adventure(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            location = request.POST['location']
            region = request.POST['region']
            distance = request.POST['distance']
            skill_level = request.POST['skill_level']
            adventure_start = request.POST['adventure_start']
            duration = request.POST['duration']
            meeting_location = request.POST['meeting_location']
            description = request.POST['description']
            # todo verify this lines up with the HTML
            activity = Activity.objects.get(id=request.POST['activity_id'])
            adventure = Adventure.objects.create(
                location=location, region=region, distance=distance, skill_level=skill_level,
                adventure_start=adventure_start, duration=duration, meeting_location=meeting_location,
                description=description, activity=activity, organizer=User.objects.get(
                    id=request.session['user_id'])
            )
            return redirect('/adventure_detail', adventure.id)
    return redirect('/adventures')
