from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from .models import Post, UserProfile, LCGlobalData
import requests
from . import models
#from django.urls import url

website_name = 'LeetCode Friends'


@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except: 
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass


    return render(request, 'main/home.html', {"posts": posts})


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()
 
    return render(request, 'main/create_post.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def index(request):
    update_lc_global_data()
    return render(request, 'main/index.html', {'website_name':'LeetCode Friends'})


def profile(request):
    return render(request, 'main/profile.html', {'website_name':'LeetCode Friends'})


def fetch_and_store_lc_user_data(request, username):
    url = 'https://leetcode-stats-api.herokuapp.com/{username}'

    response = requests.get(url)
    data = response.json()

    # Check if the API response indicates an error (user does not exist on LeetCode)
    if 'status' in data and 'message' in data and data['status'] == 'error' and data['message'] == 'user does not exist':
        return HttpResponse('LeetCode user does not exist.')

    # Process the data and save it to the database    
    # Create or update the UserProfile model instance
    UserProfile.objects.update_or_create(
        username = data['username'],
        totalSolved = data['totalSolved'],
        #totalQuestions = data['totalQuestions'],
        easySolved = data['easySolved'],
        #totalEasy = data['totalEasy'],
        mediumSolved = data['mediumSolved'],
        #totalMedium = data['totalMedium'],
        hardSolved = data['hardSolved'],
        #totalHard = data['totalHard'],
        acceptanceRate = data['acceptanceRate'],
        ranking = data['ranking'],
        contributionPoints = data['contributionPoints'],
        reputation = data['reputation'],
    )

    return HttpResponse('Data fetched and stored successfully!')

#'''
def update_lc_global_data():
    url = 'https://leetcode-stats-api.herokuapp.com/paulvaldez'

    response = requests.get(url)
    data = response.json()

    totalQuestions = data['totalQuestions']
    totalEasy = data['totalEasy']
    totalMedium = data['totalMedium']
    totalHard = data['totalHard']

    # Fetch the latest record from the database
    latest_lc_global_data = models.LCGlobalData.objects.latest('id')

    if (
        latest_lc_global_data.totalQuestions != totalQuestions or
        latest_lc_global_data.totalEasy != totalEasy or
        latest_lc_global_data.totalMedium != totalMedium or
        latest_lc_global_data.totalHard != totalHard
    ):
        # Create a new record with a new ID
        new_lc_global_data = models.LCGlobalData.objects.create(
            totalQuestions=totalQuestions,
            totalEasy=totalEasy,
            totalMedium=totalMedium,
            totalHard=totalHard,
        )

        return HttpResponse('New LCGlobalData entry created!'
                            + '<br><br>Total questions: %d' % totalQuestions
                            + '<br>Easy: %d' % totalEasy
                            + '<br>Medium: %d' % totalMedium
                            + '<br>Hard: %d' % totalHard)
    else:
        return HttpResponse('No changes in LCGlobalData')
#'''