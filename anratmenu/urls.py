from django.urls import path, register_converter

from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.AnratHome.as_view(), name='home'),
    path('menu/', views.MenuAnrat.as_view(), name='menu'),  # http://127.0.0.1:8000/
    path('about/', views.menu_abt, name='about'),
    path('contacts/', views.AnratContacts.as_view(), name='contact'),
    path('contacts/<slug:post_slug>', views.ShowContact.as_view(), name='contacts'),
    path('menu/category/<slug:cat_slug>', views.ShowDrinksCategory.as_view(), name='category_by_slug'),
    path('menu/item/<slug:item_slug>', views.ShowItem.as_view(), name='show_item'),
    path('menu/tag/<slug:tag_slug>/', views.ShowTagDrinks.as_view(), name='tag'),
    path('reviews/', views.ShowReviews.as_view(), name='reviews'),
    path('reviews/review-form/', views.ReviewForm.as_view(), name='review_form'),
    path('reviews/edit/<int:pk>/', views.UpdateReview.as_view(), name='edit_review'),
    path('reviews/delete/<int:pk>/', views.DeleteReview.as_view(), name='delete_review')
]
