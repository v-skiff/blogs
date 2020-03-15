from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        return render(request, 'main/index.html')


def index(request):
    # bbs = Bb.objects.filter(is_active=True)[:10]
    bbs = None
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)


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