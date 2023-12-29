from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Coffee, Admins, Categories, TagDrink, Review


@admin.register(Coffee)
class DrinksAdmin(admin.ModelAdmin):
    # fields = ['title', 'content', 'slug'] # добавить поля в форму редактирования
    # exclude = [] # исключить поля
    # readonly_fields = ['slug'] # сделать только для чтения поля
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = ('title', 'price', 'time_create', 'is_published', 'brief_info', 'category')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ['is_published', 'price']
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'category__title']
    list_filter = ['category__title', 'is_published']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, coffee: Coffee):
        return f"Описание {len(coffee.content)} символов"

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Coffee.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Coffee.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации", messages.WARNING)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'review_photo', 'photo', 'phone_number', 'text', 'is_published']
    list_display = ('id', 'name', 'review_photo', 'text', 'phone_number')
    list_display_links = ('id', 'name')
    ordering = ['id']
    readonly_fields = ['id', 'name', 'text', 'review_photo', 'phone_number', 'email']
    list_per_page = 5
    search_fields = ['text', 'name', 'phone_number']
    save_on_top = True

    @admin.display(description='Фото')
    def review_photo(self, review: Review):
        if review.photo:
            return mark_safe(f"<img src='{review.photo.url}' width=50>")
        else:
            return 'без фото'



# admin.site.register(Coffee, AnratAdmin)
admin.site.register(Admins)
# admin.site.register(Categories)
admin.site.register(TagDrink)
