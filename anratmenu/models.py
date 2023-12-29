from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
         'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
         'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
         'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
         'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
         'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
         'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
         'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
         'Ю': 'U', 'Я': 'YA'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Coffee.Status.PUBLISHED)


class Coffee(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Текст описания')
    photo = models.CharField(blank=True, max_length=255, verbose_name='Фото')
    category = models.ForeignKey('Categories', on_delete=models.PROTECT, related_name='drinks',
                                 verbose_name='Категория')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время редактирования')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Статус')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг(для адресной строки)')
    price = models.FloatField(default=0, verbose_name='Цена')
    tags = models.ManyToManyField('TagDrink', blank=True, related_name='drinks', verbose_name='Теги')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_item', kwargs={'item_slug': self.slug})

    class Meta:
        verbose_name = 'Коктейли и напитки'
        verbose_name_plural = 'Коктейли и напитки'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)


class Admins(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name_surname = models.CharField(max_length=50)
    photo = models.BinaryField(blank=True)
    role = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.name_surname

    def get_absolute_url(self):
        return reverse('contacts', kwargs={'post_slug': self.slug})


class Categories(models.Model):
    title = models.CharField(max_length=30, db_index=True, verbose_name='Категория')
    slug = models.SlugField(unique=True, max_length=255, db_index=True)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_by_slug', kwargs={'cat_slug': self.slug})


class TagDrink(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Review(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(max_length=255, verbose_name='Эл. почта')
    photo = models.ImageField(upload_to='reviews_photos/%Y/%m/%d', default=None, blank=True, null=True,
                              verbose_name='Фото')
    phone_number = models.IntegerField(verbose_name='Номер телефона')
    text = models.TextField(max_length=2500, verbose_name='Текст отзыва')
    is_published = models.BooleanField(default=True, verbose_name='Публичный')
    datetime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата и время написания')
    published = PublishedManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
        ordering = ['-datetime']
        indexes = [
            models.Index(fields=['-datetime'])
        ]


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')