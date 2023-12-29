menu = [{'title': 'О нас', 'url_name': 'about'},
        {'title': 'Меню бара', 'url_name': 'menu'},
        {'title': 'Контакты', 'url_name': 'contact'},
        {'title': 'Отзывы', 'url_name': 'reviews'},
        {'title': 'Войти', 'url_name': 'login'},
        ]


class DataMixin:
    paginate_by=5
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    @staticmethod
    def get_mixin_context(context, **kwargs):
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
