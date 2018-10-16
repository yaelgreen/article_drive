from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from article_drive import settings
from . import views

app_name = 'manage_article_drive'

urlpatterns = [
    # ex: /manage_article_drive/
    path('', views.index, name='index'),
    # ex: /manage_article_drive/new_articles/
    path('new_articles', views.new_articles, name='new_articles'),
    # ex: /manage_article_drive/saved_articles/
    path('saved_articles', views.saved_articles, name='saved_articles'),
    # ex: /manage_article_drive/change_tags/
    path('change_tags', views.change_tags, name='change_tags'),
    # ex: /manage_article_drive/deleted_articles/
    path('deleted_articles', views.deleted_articles, name='deleted_articles'),
    # ex: /manage_article_drive/5/
    path('<int:article_id>/', views.detail, name='detail'),
    # ex: /manage_article_drive/search_by_text/
    path('search_by_text', views.search_by_text, name='search_by_text'),
    # ex: /manage_article_drive/search_by_dates/
    path('search_by_dates', views.search_by_dates, name='search_by_dates'),
    # ex: /manage_article_drive/dates/2018/1/1/2018/10/1/
    path('dates/<int:start_year>/<int:start_month>/<int:start_day>/<str'
         ':end_year>/<int:end_month>/<int:end_day>/',
         views.saved_articles_in_date_range,
         name='saved_articles_in_date_range'),
    # ex: /manage_article_drive/contains/word1+word2/
    url(r'^contains/(?P<search_words>[\w\+]+)/$',
        views.saved_articles_contain_words,
         name='saved_articles_contain_words'),
    # saved_articles_exact_words
    url(r'^exact/(?P<search_words>[\w\+]+)/$',
        views.saved_articles_exact_words,
        name='saved_articles_exact_words'),
    #ex: /manage_article_drive/search_by_tag
    path('search_by_tag', views.search_by_tag, name='search_by_tag'),
    # ex: /manage_article_drive/manage_new_articles
    path('manage_new_articles', views.manage_new_articles,
         name='manage_new_articles'),
    # ex: /manage_article_drive/manage_new_articles/5/
    path('delete_articles', views.delete_articles, name='delete_articles'),
    # ex: /manage_article_drive/save_articles/5/
    path('save_articles', views.save_articles, name='save_articles')
]