from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CategoriesModel)
admin.site.register(ForumsModel)
admin.site.register(TopicsModel)
admin.site.register(PostsModel)