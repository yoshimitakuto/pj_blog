from django.db import models
from django.urls import reverse_lazy
# ユーザー作成に必要な記述
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField('メールアドレス', unique=True)
    
    
class Category(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="作成日",
        )
    
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="最終更新日",
        )
        
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="タイトル",
        )
        
    body = models.TextField(
        blank=True,
        null=False,
        verbose_name="本文",
        help_text="HTMLタグは使用できません。"
        )
        
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="カテゴリ",
        )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="タグ",
        )
    
    """"
     「公開・非公開設定」
    本番運用中に後から下記の設定を行わないと、既存のpostに対して公開なのか非公開なのかdjangoが判定できず、
    migration errorの原因につながるため以下の記述でdefault=Trueにする必要がある。
    """
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])
