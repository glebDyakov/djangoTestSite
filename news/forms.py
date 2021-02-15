from captcha.fields import CaptchaField,CaptchaTextInput
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django import forms
import re
from .models import Category
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class ContactForm(forms.Form):
    subject = forms.CharField(label="тема", widget=forms.TextInput(
        attrs={'class': 'form-control'}
    )))
    content = forms.CharField(label="текс", widget=forms.Textarea(
        attrs={'class': 'form-control', rows: 5}
    )))
    captcha=CaptchaField()

class UserRegisterForm(AuthenticationForm):
    username = forms.CharField( label="имя пользователя", widget=forms.Textarea(
        attrs={'class':'form-control',rows:5}
    )))
    password = forms.CharField( label="пароль",widget=forms.Textarea(
        attrs={'class':'form-control',rows:5}
    )))

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username','email','password','password2')

# class NewsForm(forms.Form):
    # title=forms.CharField(max_length=150, label="название", widget=forms.TextInput(
    #     attrs={'class':'form-control'}
    # ))
    # text = forms.CharField( label="текст",required=false,initial=True, widget=forms.Textarea(
    #     attrs={'class':'form-control',rows:5}
    # )))
    # is_published = forms.BooleanField( label="опубликовано")
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), label="категория",empty_label='выберите категорию', widget=forms.Select(
    #     attrs={'class':'form-control'}
    # )))
class NewsForm(forms.ModelForm):
    class Meta:
        model=News
        # fields='__all__'
        fields = ['title','content','is_published','category']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.TextArea(attrs={'class': 'form-control','rows':5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_title(self):
        title=self.cleaned_data['title']
        if re.match('\d',title):
            raise ValidationError('название не должно начинаться с цифры')
        return title
