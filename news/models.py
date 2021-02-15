from django.db import models
from django.urls import reverse

class News(models.Model):
    title=models.CharField(max_length=150,verbose_name="наименование")
    content=models.TextField(blank=True,verbose_name="контент")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="дата пуликации")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="обновлено")
    photo=models.ImageField(upload_to="photos/%Y/%m/%d/",verbose_name="опубликовано",blank=True)
    is_published=models.BooleanField(default=True)
    category=models.ForeignKey('Category',models.PROTECT,
                               # null=True,
                               default=1,verbose_name="категория",related_name='get_news')
    def my_func(self):
        return "hello"
    views=models.IntegerField(default=0)
    def get_absolute_url(self):
        return reverse('view_news',kwargs={"pk":self.pk})
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

class Category(models.Model):
    title=models.CharField(max_length=150,db_index=,verbose_name="наименование категории")
    def get_absolute_url(self):
        return reverse('category',kwargs={"category_id":self.pk})
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['title']


# Create your models here.
