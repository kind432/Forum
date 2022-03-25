from django import forms
from django.forms import ModelForm
from .models import *

class CategoriesForm(ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'О чем ваша категория?'}
        ),
        max_length = 100,
        help_text = 'Максимальная длина текста 100 символов.',
        label = 'Описание'
    )

    class Meta:
        model = CategoriesModel
        fields = ['title', 'description']

class ForumsForm(ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'О чем ваш форум?'}
        ),
        max_length=100,
        help_text='Максимальная длина текста 100 символов.',
        label='Описание'
    )
    class Meta:
        model = ForumsModel
        fields = ['title', 'description']

class TopicsForm(ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Сообщение'}
        ),
        max_length=4000,
        help_text='Максимальная длина текста 4000 символов.',
        label='Сообщение'
    )

    class Meta:
        model = TopicsModel
        fields = ['subject', 'message']

class PostsForm(ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5}
        ),
        max_length=4000,
        help_text='Максимальная длина текста 4000 символов.',
        label='Сообщение'
    )

    class Meta:
        model = PostsModel
        fields = ['message']

class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','email','password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']