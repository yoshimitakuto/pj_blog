# ListViewとDetailViewを取り込み
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post

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