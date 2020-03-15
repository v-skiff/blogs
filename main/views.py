from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post


class IndexView(ListView):
    context_object_name = 'users'
    paginate_by = 3
    template_name = 'main/index.html'

    def get_queryset(self):
        return User.objects.all()


class BPUserPosts(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'main/user_posts.html'

    def get_queryset(self):
        return User.objects.get(id=self.kwargs['id']).blog_posts.all().order_by('-date_pub')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user'] = User.objects.get(id=self.kwargs['id'])
        return context


class BPUserPostDetail(DetailView):
    model = Post
    template_name = 'main/user_post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
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


class BPLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    # bbs = Bb.objects.filter(author=request.user.pk)
    # context = {'bbs': bbs}
    context = {'1': 1}
    return render(request, 'main/profile.html', context)


class BPLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'