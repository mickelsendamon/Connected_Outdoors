from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
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
            'all_adventures': Adventure.objects.all().order_by('adventure_start'),
            'all_sg_equipment': SuggestedEquipment.objects.all(),
            'all_activities': Activity.objects.all(),
        }
        return render(request, "adventures.html", context)
    return redirect('/')


def join_adventure(request, adv_id):
    if 'user_id' in request.session:
        this_adventure = Adventure.objects.get(id=adv_id)
        this_adventure.participants.add(
            User.objects.get(id=request.session['user_id']))
        return redirect(f'/adventure_detail/{adv_id}')
    return redirect('/')


def leave_adventure(request, adv_id):  # todo done
    # todo clarify if this is a post or get
    if request.method == 'POST':
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            this_adventure = Adventure.objects.get(id=adv_id)
            this_adventure.participants.remove(user)
    return redirect('/my_adventures')


def my_adventures(request):  # todo done
    #  todo discuss do we want organizer to be added to participants list?

    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    my_advs = user.participated_adventures.all().order_by('adventure_start')
    context = {
        'current_user': user,
        'my_adventures': my_advs,
        'all_activities': Activity.objects.all(),
    }
    return render(request, "my_adventures.html", context)


def adventure_detail(request, adv_id):
    if 'user_id' in request.session:
        adventure = Adventure.objects.get(id=adv_id)
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'current_adventure': adventure,
            'discussion_posts': adventure.discussion_posts.order_by('-id'),
        }
        return render(request, "adventure_details.html", context)
    return redirect('/')


def cancel_adventure(request, adv_id):
    if request.method == 'POST':
        #  todo check for user in session
        if Adventure.objects.filter(id=adv_id):
            this_adventure = Adventure.objects.get(id=adv_id)
            this_adventure.delete()
            return redirect('/my_adventures')
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
    if request.method == "POST":
        if 'user_id' in request.session:
            errors = Adventure.objects.adventure_validation(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/new_adventure')
            else:
                location = request.POST['location']
                region = request.POST['region']
                distance = request.POST['distance']
                skill_level = request.POST['skill_level']
                adventure_start = request.POST['adventure_start']
                duration = request.POST['duration']
                meeting_location = request.POST['meeting_location']
                description = request.POST['description']
                sg_equipment = request.POST.getlist('suggested_equipment')

                activity = Activity.objects.get(id=request.POST['activity_id'])
                adventure = Adventure.objects.create(
                    location=location, region=region, distance=distance, skill_level=skill_level,
                    adventure_start=adventure_start, duration=duration, meeting_location=meeting_location,
                    description=description, activity=activity, organizer=User.objects.get(
                        id=request.session['user_id'],)
                )
                adventure.participants.add(
                    User.objects.get(id=request.session['user_id']))
                for equipment in sg_equipment:
                    equipment_object = SuggestedEquipment.objects.get(
                        id=equipment)
                    adventure.suggested_equipment.add(equipment_object)

                return redirect(f'/adventure_detail/{adventure.id}')
        return redirect('/')
    return redirect('/')


def create_activity(request):
    if 'user_id' in request.session:
        context = {
            "all_activities": Activity.objects.all(),
            'current_user': User.objects.get(id=request.session['user_id']),
            'all_sg_equipment': SuggestedEquipment.objects.all(),
        }
        return render(request, "activity_form.html", context)
    return redirect('/')


def add_activity(request):
    if request.method == "POST":
        new_activity = Activity.objects.create(
            name=request.POST["activity_name"], image=request.FILES["activity_image"])

        return redirect("/activity_form")


def add_sg_equipment(request):
    if request.method == "POST":
        new_equpiment = SuggestedEquipment.objects.create(
            name=request.POST['equipment_name'], description=request.POST['description']
        )
        return redirect("/activity_form")


def edit_adventure_page(request, adv_id):
    if 'user_id' in request.session:
        adventure = Adventure.objects.get(id=adv_id)
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'current_adventure': Adventure.objects.get(id=adv_id),
            'all_equipment_out': SuggestedEquipment.objects.exclude(suggested_for=adventure),
            'all_equipment_in': SuggestedEquipment.objects.filter(suggested_for=adventure)
        }
        return render(request, "edit_adventure.html", context)
    return redirect('/')


def edit_adventure(request, adv_id):
    if 'user_id' in request.session:
        if request.method == "POST":
            errors = Adventure.objects.adventure_validation(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/edit_adventure/{adv_id}')
            else:
                advenuter = Adventure.objects.get(id=adv_id)
                equipment_add = request.POST.getlist('equipment_add')
                equipment_remove = request.POST.getlist('equipment_remove')
                adventure = Adventure.objects.get(id=adv_id)
                adventure.location = request.POST['location']
                adventure.region = request.POST['region']
                adventure.distance = request.POST['distance']
                adventure.skill_level = request.POST['skill_level']
                adventure.adventure_start = request.POST['adventure_start']
                adventure.duration = request.POST['duration']
                adventure.meeting_location = request.POST['meeting_location']
                adventure.description = request.POST['description']
                for equipment in equipment_add:
                    equipment_object_add = SuggestedEquipment.objects.get(
                        id=equipment)
                    adventure.suggested_equipment.add(equipment_object_add)
                for equipment in equipment_remove:
                    equipment_object_remove = SuggestedEquipment.objects.get(
                        id=equipment)
                    adventure.suggested_equipment.remove(
                        equipment_object_remove)
                adventure.save()
        return redirect(f'/edit_adventure/{adv_id}')
    return redirect('/')


def filter_adventures(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            if 'region' in request.POST:
                region_filter = request.POST['region']
            else:
                region_filter = None
            if 'difficulty' in request.POST:
                difficulty_filter = request.POST['difficulty']
            else:
                difficulty_filter = None
            if 'activity' in request.POST:
                activity_filter = request.POST['activity']
            else:
                activity_filter = None
            if region_filter is not None:
                if difficulty_filter is not None:
                    if activity_filter is not None:
                        # all
                        adventures = Adventure.objects.filter(
                            region=region_filter, skill_level=difficulty_filter, activity__name=activity_filter
                        )
                    else:

                        # region & difficulty

                        adventures = Adventure.objects.filter(
                            region=region_filter, skill_level=difficulty_filter
                        )
                elif activity_filter is not None:
                    # region & activity
                    adventures = Adventure.objects.filter(
                        region=region_filter, activity__name=activity_filter
                    )
                else:
                    # region
                    adventures = Adventure.objects.filter(
                        region=region_filter
                    )
            elif difficulty_filter is not None:
                if activity_filter is not None:
                    # difficulty & activity
                    adventures = Adventure.objects.filter(
                        skill_level=difficulty_filter, activity__name=activity_filter
                    )
                else:
                    # difficulty
                    adventures = Adventure.objects.filter(
                        skill_level=difficulty_filter
                    )
            elif activity_filter is not None:
                # activity
                adventures = Adventure.objects.filter(
                    activity__name=activity_filter
                )
            else:
                adventures = Adventure.objects.all()
            context = {
                'current_user': User.objects.get(id=request.session['user_id']),
                'all_adventures': adventures,
                'all_sg_equipment': SuggestedEquipment.objects.all(),
                'all_activities': Activity.objects.all(),
            }
            return render(request, 'adventures.html', context)
        return redirect('/')
    return redirect('/adventures')


def filter_my_adventures(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            if 'region' in request.POST:
                region_filter = request.POST['region']
            else:
                region_filter = None
            if 'difficulty' in request.POST:
                difficulty_filter = request.POST['difficulty']
            else:
                difficulty_filter = None
            if 'activity_id' in request.POST:
                activity_filter = request.POST['activity_id']
            else:
                activity_filter = None
            if region_filter is not None:
                if difficulty_filter is not None:
                    if activity_filter is not None:
                        # all
                        adventures = Adventure.objects.filter(
                            region=region_filter, skill_level=difficulty_filter, activity__name=activity_filter
                        ).orderby()
                    else:
                        # region & difficulty
                        adventures = Adventure.objects.filter(
                            region=region_filter, skill_level=difficulty_filter
                        )
                elif activity_filter is not None:
                    # region & activity
                    adventures = Adventure.objects.filter(
                        region=region_filter, activity__name=activity_filter
                    )
                else:
                    # region
                    adventures = Adventure.objects.filter(
                        region=region_filter
                    )
            elif difficulty_filter is not None:
                if activity_filter is not None:
                    # difficulty & activity
                    adventures = Adventure.objects.filter(
                        skill_level=difficulty_filter, activity__name=activity_filter
                    )
                else:
                    # difficulty
                    adventures = Adventure.objects.filter(
                        skill_level=difficulty_filter
                    )
            elif activity_filter is not None:
                # activity
                adventures = Adventure.objects.filter(
                    activity__name=activity_filter
                )
            else:
                adventures = Adventure.objects.all()
            context = {
                'current_user': User.objects.get(id=request.session['user_id']),
                'my_adventures': adventures,
                'all_activities': Activity.objects.all(),
            }
            return render(request, 'my_adventures.html', context)
        return redirect('/')
    return redirect('/adventures')


def post_discussion(request, adv_id):
    if request.method == "POST":
        if 'user_id' in request.session:
            errors = DiscussionPost.objects.discussion_validation(request.POST)
            if len(errors) > 0:
                error_string = ''
                for error in errors:
                    error_string += f'<p>{errors[error]}</p>'
                    print(errors, error_string)
                    response = JsonResponse({'error': error_string})
                    response.status_code = 411
                return response
            adv = Adventure.objects.get(id=adv_id)
            new_post = DiscussionPost.objects.create(
                post_text=request.POST['post_text'], adventure=adv,
                posted_by=User.objects.get(id=request.session['user_id'])
            )
            context = {
                'post': new_post,
            }
            return render(request, 'discussion_snippet.html', context)
        return redirect('/')
    return redirect('/logout')


def post_reply_ajax(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            errors = DiscussionReply.objects.reply_validation(request.POST)
            if len(errors) > 0:
                error_string = ''
                for error in errors:
                    error_string += f'<p>{errors[error]}</p>'
                    print(errors, error_string)
                    response = JsonResponse({'error': error_string})
                    response.status_code = 411
                return response
            discussion = DiscussionPost.objects.get(id=request.POST['post_id'])
            adv_id = discussion.adventure.id
            DiscussionReply.objects.create(
                reply_text=request.POST['reply_text'], discussion_post=discussion,
                posted_by=User.objects.get(id=request.session['user_id'])
            )
            adventure = Adventure.objects.get(id=adv_id)
            context = {
                'discussion_posts': adventure.discussion_posts.order_by('-id'),
            }
            return render(request, 'discussion_posts.html', context)
        return redirect('/')
    return redirect('/logout')


# def post_reply(request, discussion_id):
#     if request.method == "POST":
#         if 'user_id' in request.session:
#             discussion = DiscussionPost.objects.get(id=discussion_id)
#             adv_id = discussion.adventure.id
#             DiscussionReply.objects.create(
#                 reply_text=request.POST['reply_text'], discussion_post=discussion,
#                 posted_by=User.objects.get(id=request.session['user_id'])
#             )
#             adventure = Adventure.objects.get(id=adv_id)
#             context = {
#                 'discussion_posts': adventure.discussion_posts.all(),
#             }
#             return render(request, 'discussion_posts.html', context)
#         return redirect('/')
#     return redirect('/logout')
