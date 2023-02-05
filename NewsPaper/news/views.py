from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters.filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category


class PostsList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        cat_slug = self.kwargs.get('slug')
        if ('AT' in self.request.path) or ('NW' in self.request.path):
            context = Post.objects.filter(p_type=self.kwargs['p_type'])
        elif cat_slug:
            context = Post.objects.filter(category__slug=cat_slug)
        else:
            context = Post.objects.all()
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('slug')
        if (Post.TP[0][0] in self.request.path) or (Post.TP[1][0] in self.request.path):
            context['quantity'] = Post.objects.filter(p_type=self.kwargs['p_type']).count()

        if Post.TP[0][0] in self.request.path:
            context['title'] = 'Статьи'
            context['post_type'] = Post.TP[0][0]
        elif Post.TP[1][0] in self.request.path:
            context['title'] = 'Новости'
            context['post_type'] = Post.TP[1][0]
        elif cat_slug:
            cat_name = Category.objects.get(slug=cat_slug)
            context['category'] = cat_name
            context['quantity'] = Post.objects.filter(category__slug=cat_slug).count()
        else:
            context['title'] = 'Все публикации'
            context['quantity'] = Post.objects.all().count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-time'
    template_name = 'search.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Поиск публикации'}
    paginate_by = 4


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if 'do_search' in self.request.GET:
            context['is_search'] = True
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if Post.TP[0][0] in self.request.path:
            context['title'] = 'Добавить статью'
        elif Post.TP[1][0] in self.request.path:
            context['title'] = 'Добавить новость'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        if Post.TP[0][0] in self.request.path:
            post.p_type = Post.TP[0][0]
        elif Post.TP[1][0] in self.request.path:
            post.p_type = Post.TP[1][0]
        author = Author.objects.get(author_acc=self.request.user)
        post.author = author
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'title': 'Редактировать публикацию'}


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post', )
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_page')
    extra_context = {'title': 'Удалить публикацию'}







