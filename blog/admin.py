from django.contrib import admin

from .models import Post


class PublishedFilter(admin.SimpleListFilter):
    title = 'Опубликовано'
    parameter_name = 'is_published'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_published=True)
        elif self.value() == 'no':
            return queryset.filter(is_published=False)


def publish_posts(modeladmin, request, queryset):
    queryset.update(is_published=True)


publish_posts.short_description = 'Опубликовать выбранные посты'


def unpublish_posts(modeladmin, request, queryset):
    queryset.update(is_published=False)


unpublish_posts.short_description = 'Снять с публикации выбранные посты'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_editable = ["is_published"]
    actions = [publish_posts, unpublish_posts]
