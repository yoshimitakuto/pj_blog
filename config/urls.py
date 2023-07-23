from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.models import Group, User

admin.site.site_title = '匿名ブログ 内部管理サイト'
admin.site.site_header = '匿名ブログ 内部管理サイト'
admin.site.index_title = 'メニュー'
# モデルを表示にする
admin.site.register(User)
# デフォルトのモデルを非表示にする
admin.site.unregister(Group)
# 削除操作ボタンを一括で非表示にする（誤った操作を防止するため）
admin.site.disable_action('delete_selected')


urlpatterns = [
    path('staff-admin/', admin.site.urls),
    path("", include("blog.urls")),
]
