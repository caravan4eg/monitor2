# django_app/models.py
from django.db import models
 

class Tenders(models.Model):
    number = models.TextField(unique=True)
    customer = models.TextField()
    description = models.TextField()
    price = models.CharField(max_length=255)
    deadline = models.DateField()
    country = models.CharField(max_length=255)
    url_addr = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number

    class Meta:
        # managed = False         # only reading
        db_table = 'tenders'
        ordering = ('number',)
        verbose_name = 'Тендер'
        verbose_name_plural = 'Тендеры'


class KeyWord(models.Model):
    category_name = models.CharField(max_length=150, verbose_name='Метка категории')
    category_descr = models.CharField(max_length=150, 
                                      default='',
                                      verbose_name='Описание категории')
    plus_keywords = models.TextField(verbose_name='Плюс-слова')
    minus_keywords = models.TextField(verbose_name='Минус-слова')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.category_descr}. (метка: {self.category_name})'

    class Meta:
        # managed = False         # only reading
        db_table = 'keyword'
        ordering = ['category_name']
        verbose_name = 'Категория и ключевые слова'
        verbose_name_plural = 'Категории и ключевые слова'
