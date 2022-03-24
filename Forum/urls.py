from django.urls import path

from Forum.views import *

urlpatterns = [
    path('categories/', categories_view, name='categories'),
    path('categories/new/', new_category, name='new_category'),
    path('', home_view, name='home'),
    path('category/<int:category_id>/forums/', forums_view, name='forums'),
    path('category/<int:category_id>/forums/new', new_forum, name='new_forum'),
    path('forum/<int:forum_id>/topics/', topics_view, name='topics'),
    path('forum/<int:forum_id>/topics/new', new_topic, name='new_topic'),
    path('topic/<int:topic_id>/posts/', posts_view, name='posts')
]