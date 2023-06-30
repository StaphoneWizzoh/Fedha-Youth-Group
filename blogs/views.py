from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from .models import Category, Post, Tag
from .forms import CreatePostForm


class CreatePostView(CreateView):
    form_class = CreatePostForm
    template_name = 'blogs/new_post.html'

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('blogs:homepage')

    def get_form_kwargs(self):
        kwargs = super(CreatePostView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class DetailPostView(DetailView):
    model = Post
    template_name = 'blogs/blog-detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        latest = Post.objects.order_by('-timestamp')[0:3]
        pk = self.request.user.pk

        context['categories'] = categories
        context['tags'] = tags
        context['latest'] = latest
        return context


# All posts
def homepage(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.order_by('-timestamp')
    latest = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'posts': posts,
        'latest': latest,
        'categories': categories,
        'tags': tags
    }

    return render(request, "blogs/blog.html", context)


def post(request, slug):
    specific_post = Post.objects.get(slug=slug)
    context = {
        'post': specific_post,
    }
    return render(request, "blogs/post.html", context)


def post_list(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(categories__in=[category])
    context = {
        'posts': posts,
    }
    return render(request, "blogs/post_list.html", context)


def allposts(request):
    posts = Post.objects.order_by('-timestamp')
    context = {
        'posts': posts,
    }
    return render(request, "blogs/all_posts.html", context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(overview__icontains=query)).distinct()

    context = {
        'queryset': queryset
    }
    return render(request, 'search_bar.html', context)


def about(request):
    return render(request, "blogs/about.html")
