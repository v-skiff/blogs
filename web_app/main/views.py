from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post, Subscription, ReadPost

import logging
logger = logging.getLogger(__name__)


class IndexView(ListView):
    context_object_name = 'bloggers'
    paginate_by = 3
    template_name = 'main/index.html'

    def get_queryset(self):
        return User.objects.all().exclude(pk=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['subscriptions'] = Subscription.objects.all().filter(subscriber_id=self.request.user.id).values('blogger_id')
        context['subscriptions'] = {x['blogger_id'] for x in context['subscriptions']}
        return context


class BPUserPosts(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'main/user_posts.html'

    def get_queryset(self):
        return User.objects.get(id=self.kwargs['id']).blog_posts.all().order_by('-date_pub')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        read_posts = ReadPost.objects.filter(reader_id=self.request.user.id).values('post_id')
        context['read_posts'] = {x['post_id'] for x in read_posts}
        context['user'] = User.objects.get(id=self.kwargs['id'])
        return context


class BPUserPostDetail(DetailView):
    model = Post
    template_name = 'main/user_post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        read_posts = ReadPost.objects.filter(reader_id=self.request.user.id).values('post_id')
        context['read_posts'] = {x['post_id'] for x in read_posts}
        context['back_url'] = self.request.path_info
        context['user'] = User.objects.get(id=self.kwargs['user_id'])
        return context


# Personal posts
class BPPostsList(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'main/posts.html'

    def get_queryset(self):
        return self.request.user.blog_posts.all().order_by('-date_pub')


class BPPostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'main/post_create_form.html', context={'form': form})

    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect(reverse('main:posts_list'))

        return render(request, 'blog/post_create_form.html', context={'form': bound_form})


class BPPostUpdate(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        bound_form = PostForm(instance=post)
        return render(request, 'main/post_update_form.html', context={'form': bound_form, 'post': post})

    def post(self, request, id):
        post = Post.objects.get(id=id)
        bound_form = PostForm(request.POST, instance=post)
        if bound_form.is_valid():
            bound_form.save()
            return redirect(reverse('main:posts_list'))
        return render(request, 'main/post_update_form.html', context={'form': bound_form, 'post': post})


class BPPostDelete(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        return render(request, 'main/post_delete_form.html', context={'post': post})

    def post(self, request, id):
        post = Post.objects.get(id=id)
        post.delete()
        return redirect(reverse('main:posts_list'))


# Account
class BPLoginView(LoginView):
    template_name = 'main/login.html'


class BPFeed(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'main/feed.html'

    def get_queryset(self):
        subscriptions = Subscription.objects.filter(subscriber_id=self.request.user.id).values(
            'blogger_id')
        subscriptions = {x['blogger_id'] for x in subscriptions}
        return Post.objects.filter(author_id__in=subscriptions).order_by('-date_pub')


class BPLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


# Subscribe
def subscribe(request, blogger_id):
    Subscription.objects.create(subscriber_id=request.user.id, blogger_id=blogger_id)
    return redirect(reverse('main:index') + '?page=' + request.GET['page'])


def unsubscribe(request, blogger_id):
    subscription = Subscription.objects.get(subscriber_id=request.user.id, blogger_id=blogger_id)
    subscription.delete()
    read_post = ReadPost.objects.filter(reader_id=request.user.id, author_id=blogger_id)
    read_post.delete()
    return redirect(reverse('main:index') + '?page=' + request.GET['page'])


# Read post
def read(request, post_id, author_id):
    ReadPost.objects.create(reader_id=request.user.id, post_id=post_id, author_id=author_id)
    return redirect(request.GET['back_url'])


def unread(request, post_id):
    read_post = ReadPost.objects.get(post_id=post_id)
    read_post.delete()
    return redirect(request.GET['back_url'])
