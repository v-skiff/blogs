from django.urls import path
from .views import IndexView, BPFeed, BPLoginView, BPLogoutView, BPPostsList, BPPostCreate, BPPostUpdate, BPPostDelete, BPUserPosts, BPUserPostDetail, subscribe, unsubscribe

app_name = 'main'
urlpatterns = [
    # path('accounts/post/<int:id>', BPPostsDetail.as_view(), name='post_detail'),
    path('accounts/post/delete/<int:id>', BPPostDelete.as_view(), name='post_delete'),
    path('accounts/post/update/<int:id>', BPPostUpdate.as_view(), name='post_update'),
    path('accounts/post/create/', BPPostCreate.as_view(), name='post_create'),
    path('accounts/posts/', BPPostsList.as_view(), name='posts_list'),
    path('accounts/logout/', BPLogoutView.as_view(), name='logout'),
    path('accounts/profile/', BPFeed.as_view(), name='feed'),
    path('accounts/login/', BPLoginView.as_view(), name='login'),
    path('posts/<int:user_id>/<int:pk>', BPUserPostDetail.as_view(), name='user_post_detail'),
    path('posts/<int:id>', BPUserPosts.as_view(), name='user_posts'),
    path('subscribe/<int:blogger_id>', subscribe, name='subscribe'),
    path('unsubscribe/<int:blogger_id>', unsubscribe, name='unsubscribe'),
    path('', IndexView.as_view(), name='index'),
]