from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class CategoriesModel(models.Model):
    title = models.CharField('Название', max_length=30, unique=True)
    description = models.TextField('Описание', max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forums', kwargs={'category_id': self.id})
    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ForumsModel(models.Model):
    title = models.CharField('Название', max_length=30, unique=True)
    description = models.TextField('Описание', max_length=100)
    category = models.ForeignKey(CategoriesModel, related_name="Форумы", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('topics', kwargs={'forum_id': self.id})
    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Форум'
        verbose_name_plural = 'Форумы'

class TopicsModel(models.Model):
    subject = models.CharField('Тема', max_length=255)
    last_updated = models.DateTimeField('Время последнего изменения', auto_now_add=True)
    forum = models.ForeignKey(ForumsModel, related_name='Темы', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='Темы', on_delete=models.CASCADE)



    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('posts', kwargs={'topic_id': self.id})
    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class PostsModel(models.Model):
    message = models.TextField('Сообщение', max_length=4000)
    topic = models.ForeignKey(TopicsModel, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Создано в', auto_now_add=True)
    updated_at = models.DateTimeField('Изменено в', null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    first_post = models.BooleanField(null = True)

    def __str__(self):
        return self.message
    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'