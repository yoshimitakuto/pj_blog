from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass


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