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


def adventures_page(request):  # todo Matyas & Jess
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'all_adventures': Adventure.objects.all().order_by('-adventure_start'),
            'all_sg_equipment': SuggestedEquipment.objects.all(),
            'all_activities': Activity.objects.all(),
        }
        return render(request, "adventures.html", context)
    return redirect('/')


def join_adventure(request, adv_id):
    if 'user_id' in request.session:
        this_adventure = Adventure.objects.get(id=adv_id)
        this_adventure.participants.add(User.objects.get(id=request.session['user_id']))
        return redirect(f'adventure_detail/{adv_id}')
    return redirect('/')


def leave_adventure(request, adv_id):  # todo done
    # todo clarify if this is a post or get
    if request.method == 'POST':
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            this_adventure = Adventure.objects.get(id=adv_id)
            this_adventure.participants.remove(user)
    return redirect('/adventures')


def my_adventures(request):  # todo done
    #  todo discuss do we want organizer to be added to participants list?

    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    my_advs = []
    for adv in user.organized_adventures.all():
        my_advs.append(adv)
    for adv in user.participated_adventures.all():
        my_advs.append(adv)
    context = {
        'current_user': user,
        'my_adventures': my_advs,
        'all_activities': Activity.objects.all(),
    }
    return render(request, "my_adventures.html", context)


def adventure_detail(request, adv_id):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'current_adventure': Adventure.objects.get(id=adv_id),
        }
        return render(request, "adventure_details.html", context)
    return redirect('/')


def cancel_adventure(request, adv_id):
    if request.method == 'POST':
        #  todo check for user in session
        if Adventure.objects.filter(id=adv_id):
            this_adventure = Adventure.objects.get(id=adv_id)
            this_adventure.delete()
        else:
            messages.error(request, 'Could not locate a matching Adventure')
    return redirect('/adventures')


def new_adventure(request):
    if 'user_id' in request.session:
        context = {
            'all_activities': Activity.objects.all(),
            'all_sg_equipment': SuggestedEquipment.objects.all(),
        }
        return render(request, "new_adventure.html", context)
    return redirect('/')


def create_adventure(request):  # todo add equipment
    if 'user_id' in request.session:
        if request.method == 'POST':
            location = request.POST['location']
            region = request.POST['region']
            distance = request.POST['distance']
            skill_level = request.POST['skill_level']
            adventure_start = request.POST['adventure_start']
            duration = request.POST['duration']
            meeting_location = request.POST['meeting_location']
            description = request.POST['description']
            activity = Activity.objects.get(id=request.POST['activity_id'])  # todo verify this lines up with the HTML
            adventure = Adventure.objects.create(
                location=location, region=region, distance=distance, skill_level=skill_level,
                adventure_start=adventure_start, duration=duration, meeting_location=meeting_location,
                description=description, activity=activity, organizer=User.objects.get(id=request.session['user_id'])
            )
            return redirect(f'/adventure_detail/{adventure.id}')
        return redirect('/new_adventure')
    return redirect('/')

def create_activity(request):
    context = {
        "all_activities": Activity.objects.all(),
    }
    return render(request, "activity_form.html", context)

def add_activity(request):
    if request.method == "POST":
        new_activity = Activity.objects.create(name = request.POST["activity_name"], image = request.FILES["activity_image"])
        return redirect("/activity_form")