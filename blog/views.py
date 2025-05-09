from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from blog.models import BlogPost

from django.urls import reverse
from pytils.translit import slugify
from blog.functions.utils import send_email
from catalog.views import never_cache_class


@never_cache_class
class BlogCreateView(CreateView):
    model = BlogPost
    fields = (
        "title",
        "content",
        "preview_image",
        "is_published",
        "views_count",
    )
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

@never_cache_class
class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = (
        "title",
        "content",
        "preview_image",
        "is_published",
        "views_count",
    )

    # success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:view", args=[self.kwargs.get("pk")])


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/list.html"
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count >= 300:
            send_email(self.object)

        return self.object


class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog:list")
