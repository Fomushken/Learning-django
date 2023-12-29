from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from anratmenu.forms import AddReviewForm
from anratmenu.models import Coffee, Admins, Review, TagDrink
from anratmenu.utils import DataMixin


def menu_abt(request):
    items = Coffee.published.all()#.select_related('category')
    paginator = Paginator(items, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {'page_obj': page_obj,
            'menu': DataMixin.get_mixin_context({})['menu'],
            'title': 'Меню AnRat',
            'cat_selected': 0}

    return render(request, 'anratmain/about.html', data)


class MenuAnrat(DataMixin, ListView):
    # model = Coffee
    template_name = 'anratmain/menu_bar.html'
    context_object_name = 'items'
    title_page = 'Бар AnRat - Меню'
    cat_selected = 0

    def get_queryset(self):
        return Coffee.published.all().select_related('category')


class ShowDrinksCategory(DataMixin, ListView):
    template_name = 'anratmain/category.html'
    context_object_name = 'category_items'
    allow_empty = False

    def get_queryset(self):
        return Coffee.published.filter(category__slug=self.kwargs['cat_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['category_items'][0].category
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.title,
                                      cat_selected=cat.pk)


class ShowItem(DataMixin, DetailView):
    model = Coffee
    template_name = 'anratmain/item_post.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Coffee.published, slug=self.kwargs[self.slug_url_kwarg])


class ShowTagDrinks(DataMixin, ListView):
    template_name = 'anratmain/menu_bar.html'
    context_object_name = 'items'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagDrink.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Coffee.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')


class AnratHome(DataMixin, TemplateView):
    template_name = 'anratmain/index.html'
    title_page = 'Бар AnRat'


class AnratAbout(DataMixin, TemplateView):
    template_name = 'anratmain/about.html'
    title_page = 'Бар AnRat - О нас'


class AnratContacts(DataMixin, ListView):
    template_name = 'anratmain/contact.html'
    title_page = 'Бар AnRat - Наши контакты'
    context_object_name = 'posts'

    def get_queryset(self):
        return Admins.published.all()


class ShowContact(DataMixin, DetailView):
    model = Admins
    template_name = 'anratmain/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Admins.published, slug=self.kwargs[self.slug_url_kwarg])


class AnratLogin(DataMixin, TemplateView):
    template_name = 'anratmain/login.html'
    title_page = 'Бар AnRat - Вход'


def page_not_found(request, exception):
    print(request, exception)
    return HttpResponseNotFound("<h1 align='center'>К сожалению, страница не найдена</h1>"
                                "<p align='center'>Можете обратиться к разработчику сайта и, "
                                "возможно, мы это поправим</p>")


class ShowReviews(DataMixin, ListView):
    template_name = 'anratmain/reviews.html'
    title_page = 'Бар AnRat - отзывы'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.published.all()


class ReviewForm(DataMixin, CreateView):
    form_class = AddReviewForm
    # model = Review
    # fields = '__all__'
    template_name = 'anratmain/review_form.html'
    title_page = 'Бар AnRat - Оставить отзыв'
    success_url = reverse_lazy('reviews')  # Если убрать, то перенаправит на get_absolute_url у модели если есть


class UpdateReview(DataMixin, UpdateView):
    model = Review
    fields = ['name', 'email', 'photo', 'text', 'is_published']
    template_name = 'anratmain/review_form.html'
    success_url = reverse_lazy('reviews')
    title_page = 'Редактирование отзыва'


class DeleteReview(DataMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('reviews')
    template_name = 'anratmain/review_form.html'
    title_page = 'Удалить отзыв?'
