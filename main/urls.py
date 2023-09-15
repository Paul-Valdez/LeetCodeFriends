from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin


urlpatterns = [
    path('', views.index, name='main-view'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('create-post/', views.create_post, name='create_post'),
    #path('admin/', admin.site.urls),
    path('profile/', views.profile, name='profile'),
    path('lcu/<str:username>/', views.fetch_and_store_lc_user_data, name='lcu'),
    #path('lcgd/', views.update_lc_global_data, name='lcgd'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('follow/', views.follow, name='follow'),
    path('about/', views.about, name='about'),
    path('leetcode_user_search/', views.user_search_view, name='leetcode_user_search'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('userprofile/editprofile/', views.editprofile, name='editprofile'),
]

'''
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''