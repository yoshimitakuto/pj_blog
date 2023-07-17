from django import forms

# formsのformを継承してクラスを作るとそれがフォームになる。
class TextForm(forms.Form):
    text = forms.CharField()
    search = forms.CharField()
    replace = forms.CharField()
    