from django.contrib import admin
from .models import Group, Post, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'created', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'author',
        'post',
        'text',
        'created'
    ]
    readonly_fields = ['created']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'author',
    ]
