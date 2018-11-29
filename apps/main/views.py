from django.shortcuts import render, redirect
from .models import *
import bcrypt
import json
from django.contrib import messages
from django.utils.safestring import mark_safe

def index(request):
    if not request.session.keys():
        request.session['username'] = ''
        request.session['reg_username'] = ''
        request.session['reg_email'] = ''
    return render(request, 'main/index.html')

def register_form(request, methods=['POST']):
    request.session['reg_username'] = request.POST['reg_username']
    request.session['reg_email'] = request.POST['reg_email']
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    else:
        User.objects.create(username=request.POST['reg_username'], email=request.POST['reg_email'], password_hash=bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt()))
        request.session['current_id'] = User.objects.last().id
        request.session['username'] = request.POST['reg_username']
        return redirect('/home')

def login_form(request, methods=['POST']):
    request.session['username'] = request.POST['username']
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    else:
        request.session['current_id'] = User.objects.get(username=request.session['username']).id
        return redirect('/home')

def login(request):
    return render(request, 'main/login_form.html')

def register(request):
    return render(request, 'main/register_form.html')

def home(request):

    context = {
        'user' : User.objects.get(id=request.session['current_id']),
        'questions' : Question.objects.all().exclude(user_id=request.session['current_id']).order_by('-created_at')[:3],
        'feed' : User.objects.raw('SELECT 1 AS id, followee_table.username AS followee, followship_table_1.created_at AS created_at, null AS question_user, null AS question_id, null AS question, null AS question_code, null AS response, null AS response_code FROM main_followship AS followship_table_1 JOIN main_user AS followee_table ON followship_table_1.followee_id = followee_table.id JOIN main_followship AS followship_table_2 ON followee_table.id = followship_table_2.follower_id JOIN main_user AS followee_is_following ON followship_table_2.followee_id = followee_is_following.id WHERE followship_table_1.follower_id=%s UNION SELECT 2 AS id, followee_table.username AS followee, followee_question.created_at AS created_at, followee_table.username AS question_user, followee_question.id AS question_id, followee_question.question AS question, followee_question.code AS question_code, null AS response,null AS response_code FROM main_followship AS followship_table_1 JOIN main_user AS followee_table ON followship_table_1.followee_id = followee_table.id JOIN main_question AS followee_question ON followee_question.user_id = followship_table_1.followee_id WHERE followship_table_1.follower_id=%s UNION SELECT 3 AS id, followee_table.username AS followee, followee_response.created_at AS created_at, followee_question_user.username AS question_user, followee_response_question.id AS question_id, followee_response_question.question AS question, followee_response_question.code AS question_code, followee_response.content AS response, followee_response.code AS response_code FROM main_followship AS followship_table_1 JOIN main_user AS followee_table ON followship_table_1.followee_id = followee_table.id JOIN main_response AS followee_response ON followee_response.user_id = followship_table_1.followee_id JOIN main_question AS followee_response_question ON followee_response_question.id = followee_response.question_id JOIN main_user AS followee_question_user ON followee_response_question.user_id = followee_question_user.id WHERE followship_table_1.follower_id=%s ORDER BY created_at DESC;', [request.session['current_id'], request.session['current_id'], request.session['current_id']])
    }
    return render(request, 'main/home.html', context)

def new_question(request):
    return render(request, 'main/question_form.html')

def question_form(request, methods=['POST']):
    request.session['question'] = request.POST['question'],
    request.session['question_code'] = request.POST['question_code']
    print(request.session['question_code'])
    Question.objects.create(
        user=User.objects.get(id=request.session['current_id']), 
        question=request.POST['question'],
        code=request.POST['question_code']
    )
    link = '/my_questions/'+str(request.session['current_id'])
    return redirect(link)

def my_questions(request):
    context = {
        'questions' : Question.objects.filter(user=User.objects.get(id=request.session['current_id'])).order_by('-created_at')
    }
    return render(request, 'main/my_questions.html', context)

def new_response(request, id):
    context = {
        'question' : Question.objects.get(id=id)
    }
    return render(request, 'main/response_form.html', context)

def response_form(request, methods=['POST']):
    request.session['response'] = request.POST['response']
    request.session['response_code'] = request.POST['response_code']
    Response.objects.create(
        user=User.objects.get(id=request.session['current_id']),
        question=Question.objects.get(id=request.POST['question_id']),
        content=request.POST['response'],
        code=request.POST['response_code']
    )
    link = '/question/'+request.POST['question_id']
    return redirect(link)

def question(request, id):
    context = {
        'question' : Question.objects.get(id=id),
        'responses' : Response.objects.filter(question_id=id)
    }
    return render(request, 'main/question.html', context)

def my_responses(request):
    context = {
        'responses' : Response.objects.filter(user=User.objects.get(id=request.session['current_id'])).order_by('-created_at')
    }
    return render(request, 'main/my_responses.html', context)

def delete_question(request, methods=['POST']):
    Question.objects.get(id=request.POST['question_id']).delete()
    return redirect('/my_questions')

def delete_response(request, methods=['POST']):
    Response.objects.get(id=request.POST['response_id']).delete()
    return redirect('/my_responses')

def profile(request, username):
    request.session['followship'] = 0
    followship = Followship.objects.filter(follower=User.objects.get(id=request.session['current_id']), followee=User.objects.get(username=username))
    if len(followship) < 1 and username != request.session['username']:
        print('not following')
        request.session['followship'] = 1
    elif len(followship) == 1:
        print('following')
        request.session['followship'] = 2
    context = {
        'profile' : User.objects.get(username=username),
        'followers' : Followship.objects.filter(followee=(User.objects.get(username=username))).count(),
        'feed' : Question.objects.raw('SELECT 1 AS id, id AS other_id, created_at FROM main_question WHERE user_id = (SELECT id FROM main_user WHERE username = %s) UNION SELECT 2 AS id, question_id AS other_id, created_at FROM main_response WHERE user_id = (SELECT id FROM main_user WHERE username = %s) UNION SELECT 3 AS id, main_user.username as other_id, main_followship.created_at FROM main_followship JOIN main_user ON main_followship.followee_id = main_user.id WHERE follower_id = (SELECT id FROM main_user WHERE username = %s) ORDER BY created_at DESC;', [username, username, username])
    }
    return render(request, 'main/profile.html', context)

def resume(request):
    return render(request, 'main/resume.html')

def browse(request):
    return render(request, 'main/browse.html')

def searched_questions(request, word):
    questions = Question.objects.filter(question__contains=word)
    context = {
        'questions' : Question.objects.filter(question__contains=word).order_by('-created_at'),
        'word' : word
    }
    return render(request, 'main/questions.html', context)

def search_bar(request, methods=['POST']):
    link = 'searched_questions/'+str(request.POST['word'])
    return redirect(link)

def user_questions(request, username):
    context = {
        'profile' : User.objects.get(username=username),
        'questions' : Question.objects.filter(user=User.objects.get(username=username))
    }
    return render(request, 'main/user_questions.html', context)

def user_responses(request, username):
    context = {
        'profile' : User.objects.get(username=username),
        'responses' : Response.objects.filter(user=User.objects.get(username=username))
    }
    return render(request, 'main/user_responses.html', context)

def user_following(request, username):
    context = {
        'profile' : User.objects.get(username=username),
        'followees' : Followship.objects.filter(follower=User.objects.get(username=username))
    }
    return render(request, 'main/user_following.html', context)

def follow(request, method=['POST']):
    if (request.session['username'] != request.POST['followee_username']):
        Followship.objects.create(
            follower = User.objects.get(id=request.session['current_id']), 
            followee = User.objects.get(username=request.POST['followee_username'])
        )
    link = 'profile/'+request.POST['followee_username']
    return redirect(link)

def logout(request):
    request.session.clear()
    return redirect('/')