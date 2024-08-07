from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CommentInLine(admin.StackedInline):
    model = Comment


class ReviewInLine(admin.StackedInline):
    model = Review


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'name', 'description', 'category',)
    list_editable = ('category',)
    search_fields = ('name', 'description',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'
    inlines = [
        ReviewInLine,
    ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'score',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    inlines = [
        CommentInLine,
    ]


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
