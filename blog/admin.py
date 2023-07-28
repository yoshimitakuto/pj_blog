from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models

# 自作フィルター検索機能
class PostTitleFilter(admin.SimpleListFilter):
    title = '本文'
    parameter_name = 'body_contains'
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(body__icontains=self.value())
        return queryset
    
    # 実際に画面上に表示されるもの　(('開発'→self.value(), '「開発」を含む'→画面に表示))
    def lookups(self, request, model_admin):
        return [
            ('開発', '「開発」を含む'),
            ('日記', '「日記」を含む'),
            ('個人', '「個人」を含む'),
        ]    
        

class PostInline(admin.TabularInline):
    # 表示するモデル
    model = models.Post
    # 編集するカラム
    fields = ('title', 'body')
    # 最終行で新たにポストを作成可能にする
    extra = 1
    
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    
@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


from django import forms

class PostAdminForm(forms.ModelForm):
    class Meta:
        labels = {
            'title': 'ブログタイトル',
            'name': '名前',
        }
        
    def clean(self):
        body = self.cleaned_data.get('body')
        if '>' in body:
            raise forms.ValidationError('HTMlタグは使用できません')
    


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    # 個別表示専用
    readonly_fields = ('created', 'updated')  # 読み取り専用
    # fields = ('title', 'body', 'category', 'tags', 'published', 'created', 'updated')
    fieldsets = [
        (None, {'fields': ('title',)}),
        ('コンテンツ', {'fields': ('body',)}),
        ('分類', {'fields': ('category', 'tags')}),
        ('メタ', {'fields': ('created', 'updated')}),
    ]
    # 以下が優先される
    form = PostAdminForm
    # manytomanyを指定して選択表示を見やすく
    filter_horizontal = ('tags',)
    
    def save_model(self, request, obj, form, change):
        print('before save')
        super().save_model(request, obj, form, change)
        print('after save')
        
    class Media:
        js = ('post.js',)    
    
    # 以下以降はリスト
    list_display = ('id', 'title', 'category', 'tags_summary', 'published', 'created', 'updated')
    """"
    「N+1」問題解消（ForeignKey）
    
    タプル形式で記述しているため（'',）とする必要がある。
    以下は外部キー設定をしているモデルの場合に記述をする必要がある。
    →理由：DBへのアクセス回数を減らすため。
    具体的には、list_displayで1回目のDBアクセスが走るが以下の設定を行わないと、それぞれのPostに対して、
    外部キーを一回一回参照しにいく必要があるためDBへの負荷が増える
    
    以下はforeign_keyフィールドの時のみ使用可能
    """
    list_select_related = ('category',)
    # 一覧表示画面から編集を可能にするための記述
    list_editable = ('title', 'category')
    # 検索機能
    search_fields = ('title', 'category__name', 'tags__name', 'created', 'updated')
    # 表示順設定：djangoはもともと昇順設定のため、「-」をつけることで降順に設定できる。
    # 「（）」ないの記述順序は最初の指定したもので降順表示、同じだった場合、次に記述したものの降順表示を適用という意味で記述をしている。
    ordering = ('-updated', '-created')
    list_filter = (PostTitleFilter, 'category', 'tags', 'created', 'updated')
    actions = ('publish', 'unpublish')
    
    def tags_summary(self, obj):
        # それぞれの投稿につけられているタグ全てを「aq」へ入れて
        aq = obj.tags.all()
        # 文字列に変換して「,」で区切ってつなげたものを「label」に格納する
        label = ','.join(map(str, aq))
        return label
    
    # 画面上で「tags_summary」を「tags」に変更するための記述。
    tags_summary.short_description = 'tags'
    
    
    # many to many　問題の解消用（ManyToManyField）
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # タグ一覧に対して事前にリロードをしておく
        return qs.prefetch_related('tags')
    
    def publish(self, request, queryset):
        queryset.update(published=True)
     
    publish.short_description = '公開する'
    
    def unpublish(self, request, queryset):
        queryset.update(published=False)
     
    unpublish.short_description = '下書きに戻す'  
        


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin import AdminSite

class BlogAdminSite(AdminSite):
    site_title = 'マイページ'
    site_header = 'マイページ'
    index_title = 'ホーム'
    # 「サイトを表示」を非表示
    site_url = None
    # ログイン用のデフォルトのフォームをlogin_formとして使用
    # 以下3行はスタッフログイン以外の通常のユーザーでもログイン可能にするための実装
    login_form = AuthenticationForm
    
    def has_permission(self, request):
        # 登録したユーザーだったら誰でもログイン可能にする
        return request.user.is_active
    
# モデルをインスタンス化する    
mypage_site = BlogAdminSite(name = 'mypage')    

# インスタンス化されたモデルからユーザーに見せたいモデルのみを以下で登録する。
mypage_site.register(models.Post)
mypage_site.register(models.Tag)
mypage_site.register(models.Category)