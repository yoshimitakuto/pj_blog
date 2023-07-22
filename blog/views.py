# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm, activate_user

class SignUpView(CreateView):
    form_class = SignUpForm
    # 新規登録に成功した後のリダイレクト先
    success_url = reverse_lazy('login')
    template_name = 'blog/signup.html'
    
class ActivateView(TemplateView):
    template_name = 'registration/activate.html'
    
    def get(self, request, uidb64, token, *args, **kwargs):
        # 認証トークンを検証
        result = activate_user(uidb64, token)
        # コンテクストのresultにTrue/Falseの結果を返す
        # 以下はTemplateViewそのもののgetに値を渡している。
        return super().get(request, result=result, **kwargs)   

# ListViewは一覧を簡単に作るためのView
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

# DetailViewは詳細を簡単に作るためのView
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post


from django.views.generic.edit import CreateView

class Create(CreateView):
    model = Post
    
    # 上記のモデルのうちユーザーに編集させるカラムを指定する。
    fields = ['title', 'body', 'category', 'tags']
    
from django.views.generic.edit import UpdateView

class Update(UpdateView):
    model = Post
    fields = ['title', 'body', 'category', 'tags']  
    
from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post
    # 削除成功した後のリダイレクト先
    success_url = '/'      
    
    
from django.views.generic.edit import FormView
from . import forms
 
class IndexForm(FormView):
    form_class = forms.TextForm
    template_name = 'blog/index_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        text = data['text']
        search = data['search']
        replace = data['replace'] 
        
        new_text = text.replace(search, replace)
        
        # get_context_dataでhtmlにデータを渡すパラメータが作成できる。
        ctxt = self.get_context_data(new_text=new_text, form=form)
        # 生成したcontextをhtmlに渡して、それをユーザーに返すための処理。
        return self.render_to_response(ctxt)