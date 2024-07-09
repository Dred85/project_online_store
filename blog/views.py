from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from blog.models import BlogPost


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'content',)
    success_url = reverse_lazy('blog:list')

class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'content')
    success_url = reverse_lazy('blog:list')


class BlogListView(ListView):
    model = BlogPost


class BlogDetailView(DetailView):
    model = BlogPost




class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:list')
