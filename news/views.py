from django.core.mail import send_mail
from django.contrib.auth import login,logout
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import MyMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse

from mysite.news.forms import NewsForm,UserRegisterForm
from django.views.generic import ListView,DetailView,ateView

from mysite.news.models import News, Category
from django.contrib.auth.forms import UserCreationForm,UserLoginForm
from django.contrib import messages
class UserLoginForm(AuthenticationForm):

def register(request):
    form=UserCreationForm()
    if request.method.POST:
       # form=UserCreationForm(request.POST)
       form=UserRegisterForm(request.POST)
        if form.is_valid:
            user=form.save()
            login(request,user)
            messages.success(request,'вы успешно зарегестрировались')
            return redirect('login')
        else:
            messages.error(request,'ошибка регистрации')
    else:
        # form = UserCreationForm()
        form = UserRegisterForm()
    return render(request,'news/register.html')
def user_login(request):
    if request.method == 'POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form=UserLoginForm()
            
    return render(request,'news/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')

def test(request):
    if request.method.POST:
       # form=UserCreationForm(request.POST)
       form=ContactForm(request.POST)
        if form.is_valid:
            mail=send_mail(form.cleaned_data['subject'],form.cleaned_data['content'],'b@mail.ru',['a@mail.ru'],fail_silently=True)
            if mail:
                messages.success(request,'письмо отправлено')
                return redirect('test',{'form':form})
            else:
                messages.error(request,'ошибка отправки')
        else:
            messages.error(request,'ошибка регистрации')
    else:
        # form = UserCreationForm()
        form = ContactForm()

    objects=['john','2','3','4','5','6','7','8',]
    paginator=Paginator(objects,2)
    page_num=request.GET.get('page',1)
    page_objects=paginator.get_page(page_num)
    return render(request,'news/test.html',{'page_obj':page_objects})
class HomeViews(ListView):
    mixin_prop='hello world'
    model=News
    template_name ='news/home_news_list.html'
    context_object_name = 'news'
    extra_context = {'title':'главная'}
    paginate_by = 2
    def get_context_data(self,*,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title'] = self.get_upper('гланая страница')
        # context['title']="Главная страница"
        context['mixin_prop']=self.get_prop()
        return context
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

# def index(request):
#     print(request)
#     news=News.objects.order_by('-created_at')
#     context={
#         'news':news,
#         'title':'список новостей'
#      }
#     return render(request,'news/index.html',context)

    def get_category(request):
        news = News.objects.filter(category_id=category_id)
        # categories=Category.objects.all()
        # category = Category.objects.get(pk=category.id)
        return render(request, 'news/category.html', {'news':news,'category':category})
    def view_news(request,news_id):
        news_item=get_object_or_404(News,pk=news_id)
        news_item=News.objects.get(pk=news_id)
        return render(request,'news/view_news.html',{"news_item":news_item})
    def add_news():
        if request.method == 'POST':
            form=NewsForm(request.POST)
            if form.is_valid():
                # news=News.objects.create(**form.cleaned_data)
                news=form.save()
                return redirect(news)
        else:
            form=NewsForm()
        return render(request,'news/add_news.html',{'form':form})


    # res='<h1>списоок новостей </h1>'
    # for item in news :
    #     res+=f"<div>\n<p>{item.title}</p>\n<p>{item.content}</p>\n</div>"
    # return HttpResponse(res)
    # return HttpResponse('hello world')
# def test(request):
#     print(request)
#     return HttpResponse('<h1>тестовая страница</h1>')
def contact(request):
    print(request)
    return HttpResponse('<h1>тестовая страница</h1>')

# Create your views here.
class NewsByCategory(ListView):
    paginate_by = 2
    model=News
    template_name='news/home_news_list.html'
    context_object_name='news'
    allow_empty=False
    def query_set(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],is_published=True).select_related('category')
    def get_context_data(self,*,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']=self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context
class ViewNews(DetailView):
    model=News
    # pk_url_kwarg ='news_id'
    template_name ='news_detail.html'
    # context_object_name = 'item'
class CreateNews(LoginRequiredMixin,CreateView):
    form_class=NewsForm
    template_name='news/add_news.html'
    success_url = reverse_lazy('home')
    login_url=reverse_lazy('/admin/')
    raise_exception=True
