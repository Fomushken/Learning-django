import copy

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.deconstruct import deconstructible

from anratmenu.models import Review


# from .models import


# @deconstructible
# class PhoneNumberValidator:
#     code = 'phone'
#
#     def __init__(self, number=None):
#         self.number = number if number else 'Номер должен содержать как минимум 10 цифр'
#
#     def __call__(self, value, *args, **kwargs):
#         if not (len(str(value)) >= 10):
#             raise ValidationError(self.number, code=self.code)

class AddReviewForm(forms.ModelForm):
    # name = forms.CharField(min_length=3, max_length=255,
    #                        label='Имя',
    #                        widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                        error_messages={
    #                            'min_length': 'Слишком короткое имя',
    #                            'required': 'Имя ввести нужно обязательно'
    #                        })
    # email = forms.EmailField(max_length=255, label='Эл. почта')
    # phone_number = forms.IntegerField(required=True, label='Номер телефона',
    #                                   error_messages={'required': 'Номер телефона обязателен, так мы сможем с вами '
    #                                                               'связаться и сделать все возможное, чтобы исправить'
    #                                                               ' ситуацию'},
    #                                   # validators=[
    #                                       # PhoneNumberValidator()
    #                                   # ]
    #                                   )
    # text = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), label='Отзыв')
    # is_published = forms.BooleanField(required=False, initial=True, label='Публичный отзыв')

    class Meta:
        model = Review
        fields = ['name', 'email', 'phone_number', 'text', 'photo', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        # labels = {'name': 'Имя'}

    # def clean_phone_number(self):
    #     phone_numberi = self.cleaned_data['phone_number']
    #     if not (len(str(phone_numberi)) >= 10):
    #         raise ValidationError('Номер должен содержать как минимум 10 цифр')
