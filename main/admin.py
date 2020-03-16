from django.contrib import admin
from .models import Post, Subscription


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_pub')
    list_filter = ('title', 'author', 'date_pub')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'date_pub'
    ordering = ('date_pub',)


admin.site.register(Subscription)