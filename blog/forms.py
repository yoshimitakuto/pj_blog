from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError

# UserCreateFormは、djangoがもともと用意している新規登録フォーム
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings

# 通常であれば「from .models import User」でUserモデルを取得するが、
# userモデルを取得する際は「get_user_model」を使用して取得するようにする必要がある。
User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        return user


# html側に自分が独自で作ったテキストを渡すためにはwidgetを独自で定義する必要がある。
widget_textarea = forms.Textarea(
    attrs= {
        # 今回はクラスhtmlへ渡したいため以下記述。
        'class': 'form-control' #bootstrapのformの記述。
    }
)
widget_textinput = forms.TextInput(
    attrs= {
        # 今回はクラスhtmlへ渡したいため以下記述。
        'class': 'form-control' #bootstrapのformの記述。
    }
)

# formsのformを継承してクラスを作るとそれがフォームになる。
class TextForm(forms.Form):
    # widgetでformの見た目を変えることができる。
    text = forms.CharField(label='', widget=widget_textarea)
    search = forms.CharField(label='検索', widget=widget_textinput)
    replace = forms.CharField(label='置換', widget=widget_textinput)
    
    # ユーザーからデータが送信された時に自動的に以下の関数が呼ばれる。
    def clean(self):
        data = super().clean()
        text = data['text']
        if len(text) <= 5:
            raise ValidationError('テキストが短すぎます。6文字以上で入力してください。')
        return data
    