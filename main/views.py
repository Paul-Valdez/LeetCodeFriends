from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import RegisterForm, PostForm, UserSearchForm
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
    #update_lc_global_data()
    return render(request, 'main/index.html', {'website_name':'LeetCode Friends'})


def profile(request):
    return render(request, 'main/profile.html', {'website_name':'LeetCode Friends'})


def fetch_and_store_lc_user_data(request, username):
    url = 'https://leetcode-stats-api.herokuapp.com/{}'.format(username)

    response = requests.get(url)
    data = response.json()

    # Check if the API response indicates an error (user does not exist on LeetCode)
    if data['status'] == 'error' and data['message'] == 'user does not exist':
        return HttpResponse("LeetCode user '<span style='color: red;'>{}</span>' does not exist.".format(username))


    # Process the data and save it to the database    
    # Create or update the UserProfile model instance
    UserProfile.objects.update_or_create(
        username = username,
        totalSolved = data['totalSolved'],
        easySolved = data['easySolved'],
        mediumSolved = data['mediumSolved'],
        hardSolved = data['hardSolved'],
        acceptanceRate = data['acceptanceRate'],
        ranking = data['ranking'],
        contributionPoints = data['contributionPoints'],
        reputation = data['reputation'],
    )

    return HttpResponse('Data fetched and stored successfully!')


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

    # if new data is different from last entry, create new ID with updated data
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
'''
        return HttpResponse('New LCGlobalData entry created!'
                            + '<br><br>Total questions: %d' % totalQuestions
                            + '<br>Easy: %d' % totalEasy
                            + '<br>Medium: %d' % totalMedium
                            + '<br>Hard: %d' % totalHard)
    else:
        return HttpResponse('No changes in LCGlobalData')
'''


def FAQ(request):
    return render(request, 'main/FAQ.html', {'website_name':'LeetCode Friends'})


def follow(request):
    return render(request, 'main/follow.html', {'website_name':'LeetCode Friends'})

'''
def user_search_view(request):
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # Add your logic here to search for the user based on the provided username
            # For example, you can use a Django query to fetch the user from the database.
            # Then pass the user object or the relevant data to be displayed.
            # Replace 'searched_user_data' with the data you want to return in the AJAX response.

            url = 'https://leetcode-stats-api.herokuapp.com/{}'.format(username)

            response = requests.get(url)
            data = response.json()

            # Check if the API response indicates an error (user does not exist on LeetCode)
            if data['status'] == 'error' and data['message'] == 'user does not exist':
                return HttpResponse("LeetCode user '<span style='color: red;'>{}</span>' does not exist.".format(username))


            # Process the data and save it to the database    
            # Create or update the UserProfile model instance
            UserProfile.objects.update_or_create(
                username = username,
                totalSolved = data['totalSolved'],
                easySolved = data['easySolved'],
                mediumSolved = data['mediumSolved'],
                hardSolved = data['hardSolved'],
                acceptanceRate = data['acceptanceRate'],
                ranking = data['ranking'],
                contributionPoints = data['contributionPoints'],
                reputation = data['reputation'],
            )



            searched_user_data = None  # Replace None with the retrieved user data.
            return JsonResponse({'searched_user_data': searched_user_data})
        else:
            return JsonResponse({'error': 'Invalid form data'})
    else:
        form = UserSearchForm()

    return render(request, 'main/leetcode_user_search.html', {'form': form})
'''


def user_search_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # Perform any processing you need for the username (e.g., validate, format)

        # Fetch the external website's page using requests
        external_url = f'https://leetcode.com/{username}'
        response = requests.get(external_url)

        # Get the HTML content of the external page
        external_html = response.content.decode('utf-8')

        return render(request, 'main/leetcode_user_search.html', {'username': username, 'external_html': external_html})

    return render(request, 'main/leetcode_user_search.html')


def about(request):
    return render(request, 'main/about.html', {'website_name':'LeetCode Friends'})


def userprofile(request):
    return render(request, 'main/userprofile.html', {'website_name':'LeetCode Friends'})


def editprofile(request):
    return render(request, 'main/editprofile.html', {'website_name':'LeetCode Friends'})