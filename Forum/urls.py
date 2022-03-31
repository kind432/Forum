from django.urls import path

from Forum.views import *

urlpatterns = [
    path('categories/', categories_view, name='categories'),
    path('categories/new/', new_category, name='new_category'),
    path('categories/update/<int:category_id>/', category_update, name='category_update'),
    path('categories/delete/<int:category_id>/', category_delete, name='category_delete'),
    path('', home_view, name='home'),
    path('category/<int:category_id>/forums/', forums_view, name='forums'),
    path('category/<int:category_id>/forums/new', new_forum, name='new_forum'),
    path('forum/update/<int:forum_id>',forum_update,name='forum_update'),
    path('forum/delete/<int:forum_id>',forum_delete,name='forum_delete'),
    path('forums/<int:forum_id>/topics/', topics_view, name='topics'),
    path('forums/<int:forum_id>/topics/new', new_topic, name='new_topic'),
    path('topic/<int:topic_id>/posts/', posts_view, name='posts'),
    path('topic/update/<int:topic_id>',topic_update,name='topic_update'),
    path('topic/delete/<int:topic_id>',topic_delete,name='topic_delete'),
    path('post/update/<int:post_id>',post_update,name='post_update'),
    path('post/delete/<int:post_id>',post_delete,name='post_delete'),
    path('user/',user_page,name='user_page'),
    path('changepassword/',user_change_password,name='change_password'),

]