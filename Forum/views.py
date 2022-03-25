from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *
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
    except CategoriesModel.DoesNotExist:
        raise Http404
    context = {
        'title': 'Категории',
        'categories': categories,
    }
    return render(request, 'categories/categories.html', context)

#Новая категория
def new_category(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoriesForm()
    return render(request, 'categories/new_category.html', context={'form': form})
#изменение категории
def category_update(request,category_id):
    try:
        old_data = get_object_or_404(CategoriesModel,id = category_id)
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
            'form': form
        }
        return render(request, 'change.html', context)

#Удаление категории
def category_delete(request, category_id):
    try:
        data = get_object_or_404(CategoriesModel,id=category_id)
    except Exception:
        raise Http404('Category not find')
    if request.method == 'POST':
        data.delete()
        return redirect('categories')
    else:
        return render(request, 'delete.html')
#Форумы
def forums_view(request, category_id):
    try:
        forums = ForumsModel.objects.filter(category = category_id)
        category = CategoriesModel.objects.get(id = category_id)
    except ForumsModel.DoesNotExist:
        raise Http404
    context = {
        'title': 'Форумы',
        'forums': forums,
        'category': category,
        'category_id': category_id,
    }
    return render(request, 'forums/forums.html', context)

def new_forum(request, category_id):
    category = get_object_or_404(CategoriesModel, id=category_id)
    if request.method == 'POST':
        form = ForumsForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.category = category
            forum.save()
            return redirect('forums', category_id = category.id)
    else:
        form = ForumsForm()
    return render(request, 'forums/new_forum.html', context={'form': form})
#изменение форума
def forum_update(request,forum_id):
    try:
        old_data = get_object_or_404(ForumsModel,id = forum_id)
    except Exception:
        raise Http404('Forum Not Found')
    if request.method == 'POST':
        form = ForumsForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = ForumsForm(instance=old_data)
        context = {
            'form': form
        }
        return render(request, 'change.html', context)

#Удаление форума
def forum_delete(request, forum_id):
    try:
        data = get_object_or_404(ForumsModel,id=forum_id)
    except Exception:
        raise Http404('Forum not find')
    if request.method == 'POST':
        data.delete()
        return redirect('categories')
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
        'forum_id': forum_id,
        'category_id': category.id,
        'forum': forum,
        'category': category,
    }
    return render(request, 'topics/topics.html', context)

def new_topic(request, forum_id):
    forum = get_object_or_404(ForumsModel, id=forum_id)
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
                created_by=user
            )
            return redirect('topics', forum_id=forum.id)
    else:
        form = TopicsForm()
    return render(request, 'topics/new_topic.html', {'forum': forum, 'form': form})
#изменение топика
def topic_update(request,topic_id):
    try:
        old_data = get_object_or_404(TopicsModel,id = topic_id)
    except Exception:
        raise Http404('Topic Not Found')
    if request.method == 'POST':
        form = TopicsForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = TopicsForm(instance=old_data)
        context = {
            'form': form
        }
        return render(request, 'change.html', context)

#Удаление топика
def topic_delete(request, topic_id):
    try:
        data = get_object_or_404(TopicsModel,id=topic_id)
    except Exception:
        raise Http404('Category not find')
    if request.method == 'POST':
        data.delete()
        return redirect('categories')
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
        form = PostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = user
            post.save()
            return redirect('posts', topic_id = topic.id)
    else:
        form = PostsForm()

    context = {
        'title': 'Ответы',
        'posts': posts,
        'form': form,
        'category_id': forum.category.id,
        'forum_id': forum.id,
        'topic_id': topic.id,
        'topic': topic,
        'forum': forum,
        'category': category,
    }
    return render(request, 'posts/posts.html', context)
#изменение поста
def post_update(request,post_id):
    try:
        old_data = get_object_or_404(PostsModel,id = post_id)
    except Exception:
        raise Http404('Post Not Found')
    if request.method == 'POST':
        form = PostsForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = PostsForm(instance=old_data)
        context = {
            'form': form
        }
        return render(request, 'change.html', context)

#Удаление категории
def post_delete(request, post_id):
    try:
        data = get_object_or_404(PostsModel,id=post_id)
    except Exception:
        raise Http404('Post not find')
    if request.method == 'POST':
        data.delete()
        return redirect('categories')
    else:
        return render(request, 'delete.html')