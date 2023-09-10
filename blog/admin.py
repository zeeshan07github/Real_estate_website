from django.contrib import admin
from .models import Post, Comment ,Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author')
    list_filter = ('pub_date', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'pub_date'
    ordering = ['pub_date' , 'author']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('post__title', 'content', 'author__username')
    ordering = ['pub_date' , 'author']

class TagAdmin(admin.ModelAdmin):
    list_display = ('name' ,)

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
