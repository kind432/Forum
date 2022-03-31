import datetime

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
import requests
import json
from .forms import *
from .models import *
from ForumProject.settings import api_url
# Create your views here.

#Главная страница
def home_view(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'home.html', context)

#Категории
def categories_view(request):
    try:
        categories = CategoriesModel.objects.all()
        print(categories)
    except CategoriesModel.DoesNotExist:
        raise Http404
    context = {
        'title': 'Категории',
        'categories': categories,
    }
    return render(request, 'categories/categories.html', context)
@permission_required('Forum.add_categoriesmodel')

#Новая категория
def new_category(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoriesForm()
        context = {
            'title': 'Новая категория',
            'form': form,
        }
    return render(request, 'categories/new_category.html', context)

#изменение категории
@permission_required('Forum.change_categoriesmodel')
def category_update(request,category_id):
    try:
        old_data = get_object_or_404(CategoriesModel, id=category_id)
    except Exception:
        raise Http404('Category Not Found')
    if request.method == 'POST':
        form = CategoriesForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoriesForm(instance=old_data)
        context = {
            'title': 'Изменение категории',
            'form': form,
            'old_category': old_data,
        }
    return render(request, 'categories/change.html', context)

@permission_required('Forum.delete_categoriesmodel')

#Удаление категории
def category_delete(request, category_id):
    try:
        data = get_object_or_404(CategoriesModel, id=category_id)
    except Exception:
        raise Http404('Категория не найдена')
    if request.method == 'POST':
        data.delete()
        return redirect('categories')
    else:
        return render(request, 'delete.html')

#Форумы
def forums_view(request, category_id):
    try:
        forums = ForumsModel.objects.filter(category=category_id)
        category = CategoriesModel.objects.get(id=category_id)
    except ForumsModel.DoesNotExist:
        raise Http404
    context = {
        'title': 'Форумы',
        'forums': forums,
        'category': category,
    }
    return render(request, 'forums/forums.html', context)

#Новый форум
@permission_required('Forum.add_forumsmodel')
def new_forum(request, category_id):
    category = get_object_or_404(CategoriesModel, id=category_id)
    if request.method == 'POST':
        form = ForumsForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.category = category
            forum.save()
            return redirect('forums', category_id=category.id)
    else:
        form = ForumsForm()
        context = {
            'title': 'Новый форум',
            'form': form,
            'category': category,
        }
    return render(request, 'forums/new_forum.html', context)

#Изменение форума
@permission_required('Forum.change_forumsmodel')
def forum_update(request,forum_id):
    try:
        old_data = get_object_or_404(ForumsModel,id=forum_id)
        category = get_object_or_404(CategoriesModel, id=old_data.category.id)
    except Exception:
        raise Http404('Forum Not Found')
    if request.method == 'POST':
        form = ForumsForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect('forums', category.id)
    else:
        form = ForumsForm(instance=old_data)
        context = {
            'title': 'Изменение форума',
            'form': form,
            'category': category,
            'old_forum': old_data,
        }
        return render(request, 'forums/change.html', context)

#Удаление форума
@permission_required('Forum.delete_forumsmodel')
def forum_delete(request, forum_id):
    try:
        data = get_object_or_404(ForumsModel,id=forum_id)
        category_id = data.category.id
    except Exception:
        raise Http404('Форум не найден')
    if request.method == 'POST':
        data.delete()
        return redirect('forums', category_id)
    else:
        return render(request, 'delete.html')

#Темы
def topics_view(request, forum_id):
    try:
        topics = TopicsModel.objects.filter(forum=forum_id)
        forum = ForumsModel.objects.get(id=forum_id)
        category = CategoriesModel.objects.get(id=forum.category.id)
    except TopicsModel.DoesNotExist:
        raise Http404
    context = {
        'title': 'Темы',
        'topics': topics,
        'forum': forum,
        'category': category,
    }
    return render(request, 'topics/topics.html', context)

#Новый топик
@permission_required('Forum.add_topicsmodel')
def new_topic(request, forum_id):
    forum = get_object_or_404(ForumsModel, id=forum_id)
    category = get_object_or_404(CategoriesModel, id=forum.category.id)
    user = request.user
    if request.method == 'POST':
        form = TopicsForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.starter = user
            topic.save()
            post = PostsModel.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user,
            )
            return redirect('topics', forum_id=forum.id)
    else:
        form = TopicsForm()
        context = {
            'title': 'Новая тема',
            'category': category,
            'forum': forum,
            'form': form,
        }
    return render(request, 'topics/new_topic.html', context)

#изменение топика
@permission_required('Forum.change_topicsmodel')
def topic_update(request,topic_id):
    f_message = PostsModel.objects.filter(topic_id=topic_id)
    first_message = f_message[0]
    try:
        old_data = get_object_or_404(TopicsModel,id=topic_id)
        forum = get_object_or_404(ForumsModel, id=old_data.forum.id)
        category = get_object_or_404(CategoriesModel, id=forum.category.id)
    except Exception:
        raise Http404('Тема не найдена')
    if request.method == 'POST':
        form = TopicsForm(request.POST, instance=old_data)
        if form.is_valid():

            first_message.message = form.cleaned_data.get('message')
            first_message.updated_at = timezone.now()
            first_message.updated_by = request.user
            first_message.save()
            form.save()
            return redirect('topics', forum_id=forum.id)
    else:
        print(first_message.message)
        data = {
            'subject': old_data.subject,
            'message': first_message.message
        }
        form = TopicsForm(data)
        context = {
            'title': 'Изменение темы',
            'form': form,
            'category': category,
            'forum': forum,
            'old_topic': old_data,
        }
        return render(request, 'topics/change.html', context)


#Удаление топика
@permission_required('Forum.delete_topicsmodel')
def topic_delete(request, topic_id):
    try:
        data = get_object_or_404(TopicsModel,id=topic_id)
        forum_id = data.forum.id
    except Exception:
        raise Http404('Тема не найдена')
    if request.method == 'POST':
        data.delete()
        return redirect('topics', forum_id)
    else:
        return render(request, 'delete.html')

#посты
def posts_view(request, topic_id):
    try:
        topic = get_object_or_404(TopicsModel, id=topic_id)
        forum = ForumsModel.objects.get(id=topic.forum.id)
        category = CategoriesModel.objects.get(id=forum.category.id)
        posts = PostsModel.objects.filter(topic=topic_id)
    except PostsModel.DoesNotExist:
        raise Http404
    user = request.user
    if request.method == 'POST':
        if user.groups.all():
            form = PostsForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.topic = topic
                post.created_by = user
                post.save()
                return redirect('posts', topic_id=topic.id)
        else:
            return render(request,'posts/error.html')
    else:
        form = PostsForm()
    context = {
        'title': 'Ответы',
        'posts': posts,
        'form': form,
        'topic': topic,
        'forum': forum,
        'category': category,
    }
    return render(request, 'posts/posts.html', context)

#изменение поста
@permission_required('Forum.change_postsmodel')
def post_update(request,post_id):
    try:
        old_data = get_object_or_404(PostsModel,id=post_id)
        topic = get_object_or_404(TopicsModel, id=old_data.topic.id)
        forum = get_object_or_404(ForumsModel, id=topic.forum.id)
        category = get_object_or_404(CategoriesModel, id=forum.category.id)
    except Exception:
        raise Http404('Пост не найден')
    if request.method == 'POST':
        old_data.updated_by=request.user
        old_data.updated_at= timezone.now()
        form = PostsForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect('posts', topic_id=topic.id)
    else:
        form = PostsForm(instance=old_data)
        context = {
            'title': 'Изменение ответа',
            'form': form,
            'category': category,
            'forum': forum,
            'topic': topic,
            'old_post': old_data,
        }
        return render(request, 'posts/change.html', context)

#Удаление поста
@permission_required('Forum.delete_postsmodel')
def post_delete(request, post_id):
    try:
        data = get_object_or_404(PostsModel,id=post_id)
        topic_id = data.topic.id
    except Exception:
        raise Http404('Пост не найден')
    if request.method == 'POST':
        data.delete()
        return redirect('posts', topic_id)
    else:
        return render(request, 'delete.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            g = Group.objects.get(name="Members")
            g.user_set.add(new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

def user_page(request):
    try:
        user = request.user

    except User.DoesNotExist:
        raise Http404
    context = {
        'title': 'Пользователь',
        'user': user,
    }
    return render(request, 'registration/userpage.html', context)


def user_change_password(request):
    form = UserChangePasswordForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data.get('new_password') != form.cleaned_data.get('new_password2'):
                raise forms.ValidationError('Passwords don\'t match.')
            user = request.user
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            return render(request, 'registration/login.html')

    else:
        form = UserChangePasswordForm()
    return render(request, 'registration/password_reset.html', {'form':form})

def news_view(request):
    response = requests.get(api_url, verify=False).json()
    query_set = []
    for i in range(len(response["articles"])):

        new = data(response["articles"][i]["source"]["name"], response["articles"][i]["author"],
                   response["articles"][i]["title"], response["articles"][i]["description"],
                   response["articles"][i]["url"], response["articles"][i]["publishedAt"])
        query_set.append(new)
    context ={
        'title': 'Новости',
        'forms': query_set
    }
    return render(request, 'news.html', context)
