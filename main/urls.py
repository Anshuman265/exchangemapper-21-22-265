from django.urls import path, include

from . import views
from .views import *
from django.views.generic import TemplateView
# decorators
from django.contrib.auth.decorators import login_required

app_name = 'main'
urlpatterns = [
    # BASIC

    # login button
    path('', views.render_login_button, name='login_button'),
    path('captcha/', include('captcha.urls')),
    path('mapper/', views.home, name='mapper_home'),
    path('guide/', login_required(TemplateView.as_view(template_name="main/guide_new.html")), name='guide'),
    # home url
    #path('home', views.home, name='home'),
    #path('search/', views.SearchResultsView.as_view(),name="search_results"),
    # path('form/',views.userinput,name="userinput"),
    # path('blog/',views.BlogListView.as_view(),name='blog'),
    path('blogs/', views.blog, name='blog'),
    #path('search/', views.SearchResultsView.as_view(),name="searchresults"),
    # path('home/',views.userinput,name='home'),
    #path('university', views.university, name = 'university'),
    #path('blog/<int:pk>/detail/', BlogDetailView.as_view(), name='experience-detail'),
    path('blog/<int:pk>/', views.blog_detail_view, name='experience-detail'),
    path('add_your_CM', views.yourExperience, name='your_exp'),
    path('write_blog/', views.experienceform, name='fill_exp'),
    # path('add_uni/',views.addUniversity, name = 'add_uni'),
    path('forum/', views.query_view, name='doubt'),
    path('query_form/', views.doubt_form_view, name='doubt-form'),
    path('f_answer/<int:pk>', views.answer_view, name='answer'),
    path('f_answerform/<int:id>', views.answer_view_form, name='answer-form'),
    path('upvote/<int:pk>/<int:id>', views.upvote_view, name='upvote'),
    path('downvote/<int:pk>/<int:id>', views.downvote_view, name='downvote'),
    path('team/', views.team_view, name='team'),
]
