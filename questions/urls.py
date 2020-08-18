from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('ask', views.ask, name="ask"),
    path('question/<int:question_id>', views.QuestionDetail.as_view(), name="question"),
    path('answer/<int:question_id>', views.answer, name="answer"),
    path('answer/upvote', views.Upvote.as_view(), name='upvote'),
    path('answer/downvote', views.Downvote.as_view(), name='downvote'),
    path('answer/unvote', views.Unvote.as_view(), name='unvote'),
    path('search', views.Search.as_view(), name='search'),
]
