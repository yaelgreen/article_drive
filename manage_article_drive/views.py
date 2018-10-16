import datetime
from django.shortcuts import render, render_to_response
from django.db.models import Q
from django.http import Http404

from manage_article_drive.forms import MultipleSelectCheckboxForm, \
    SearchDatesForm, SearchTextForm
from manage_article_drive.models import Article, Tag


def index(request): # show all saved_articles with status 0 (no choice had been made)
    # return render(request, 'manage_article_drive/index.html',)
    tags = Tag.objects.all().order_by('tag_text')
    context = {'tags': tags}
    return render(request, 'manage_article_drive/index.html', context)


def new_articles(request): # show all saved saved_articles
    tags = Tag.objects.all().order_by('tag_text')
    latest_article_list = Article.objects.filter(state=0).order_by(
        '-pub_date')
    context = {'latest_article_list': latest_article_list, 'tags': tags}
    return render(request, 'manage_article_drive/new_articles.html', context)


def change_tags(request):
    form = MultipleSelectCheckboxForm(request.POST)
    for article in form.cleaned_data['select']:
        print(article.title_text)
    # if request.method == 'POST':
    #     tag_select1 = request.POST.get('tag_select')
    #     print(tag_select1)
    #     tag_select2 = request.POST.get('tag_select')
    #     print(tag_select2)

    tags = Tag.objects.all().order_by('tag_text')
    context = {'tags': tags}
    return render(request, 'manage_article_drive/index.html', context)


def saved_articles(request): # show all saved saved_articles
    tags = Tag.objects.all().order_by('tag_text')
    latest_article_list = Article.objects.filter(state=1).order_by(
        '-pub_date')
    context = {'latest_article_list': latest_article_list, 'tags': tags}
    return render(request, 'manage_article_drive/saved_articles.html', context)


def deleted_articles(request): # show all saved_articles with status 2 (# discarded)
    latest_article_list = Article.objects.filter(state=2).order_by(
        '-pub_date')
    context = {'latest_article_list': latest_article_list}
    return render(request, 'manage_article_drive/deleted_articles.html', context)


def saved_articles_in_date_range(request, start_year, start_month,
                                 start_day, end_year, end_month, end_day):
    latest_article_list = Article.objects.filter(state=1).filter(
        pub_date__gte=datetime.date(int(start_year), int(start_month),
                                    int(start_day)),
        pub_date__lte=datetime.date(int(end_year), int(end_month),
                                    int(end_day))).order_by(
        '-pub_date')
    context = {'latest_article_list': latest_article_list}
    return render(request, 'manage_article_drive/saved_articles.html', context)


def saved_articles_contain_words(request, search_words):
    latest_article_list = []
    list_of_words = search_words.split("+")
    saved_article_list = Article.objects.filter(state=1).order_by(
        '-pub_date')
    for article in saved_article_list:
        if any(word in article.title_text for word in list_of_words):
            latest_article_list.append(article)
    context = {'latest_article_list': latest_article_list}
    return render(request, 'manage_article_drive/saved_articles.html', context)


def search_by_tag(request):
    if request.method == 'POST':
        tag_select_1 = request.POST.get('tag_select1')
        tag_select_2 = request.POST.get('tag_select2')
        tag_select_3 = request.POST.get('tag_select3')
        latest_article_list = Article.objects.filter(state=1).filter(
            Q(tags__tag_text=tag_select_1) | Q(tags__tag_text=tag_select_2) |
            Q(tags__tag_text=tag_select_3)).order_by(
            '-pub_date')
        context = {'latest_article_list': latest_article_list}
        return render(request, 'manage_article_drive/saved_articles.html',
                      context)
    return render(request, 'manage_article_drive/index.html', )


def saved_articles_exact_words(request, search_words):
    latest_article_list = []
    phrase = search_words.replace("+", " ")
    print("phrase: "+phrase)
    saved_article_list = Article.objects.filter(state=1).order_by('-pub_date')
    for article in saved_article_list:
        if phrase in article.title_text:
            latest_article_list.append(article)
            print("found "+search_words+" in "+article.title_text)
    context = {'latest_article_list': latest_article_list}
    return render(request, 'manage_article_drive/saved_articles.html', context)


def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'manage_article_drive/detail.html', {'article': article})


def search_by_dates(request):
    if request.method == 'POST':
        form = SearchDatesForm(request.POST)
        if form.is_valid():
            if request.POST.get("search_by_dates"):
                print("btn search_for_dates")
                start_d = form.cleaned_data['start_date']
                end_d = form.cleaned_data['end_date']
                return saved_articles_in_date_range(request, start_d.year,
                                                    start_d.month, start_d.day,
                                                    end_d.year, end_d.month,
                                                    end_d.day)
        else:
            print("Form invalid")
            return render_to_response(
                'manage_article_drive/show_form_errors.html', {'form': form})
    print("method: "+request.method)
    return render(request, 'manage_article_drive/index.html', )


def search_by_text(request):
    if request.method == 'POST':
        form = SearchTextForm(request.POST)
        if form.is_valid():
            if request.POST.get("search_phrase_any"):
                print("btn search_phrase_any")
                phrase = form.cleaned_data['search_phrase']
                print(phrase)
                return saved_articles_contain_words(request, phrase)
            elif request.POST.get("search_phrase_exact"):
                print("btn search_phrase_exact")
                phrase = form.cleaned_data['search_phrase']
                print(phrase)
                return saved_articles_exact_words(request, phrase)
            else:
                print("can't find btn")
        else:
            print("Form invalid")
            return render_to_response(
                'manage_article_drive/show_form_errors.html', {'form': form})
    print("method: "+request.method)
    return render(request, 'manage_article_drive/index.html', )


def manage_new_articles(request):
    form = MultipleSelectCheckboxForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        for article in form.cleaned_data['select']:
            article.state = 1 # Save it
            article.save()
        for article in Article.objects.filter(state=0):
            article.state = 2 # Delete it
            article.save()
        return saved_articles(request)
    return render(request, 'manage_article_drive/index.html', )


def delete_articles(request):
    form = MultipleSelectCheckboxForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        for article in form.cleaned_data['select']:
            article.state = 2 # Delete it
            article.save()
        return saved_articles(request)
    return render(request, 'manage_article_drive/index.html', )


def save_articles(request):
    form = MultipleSelectCheckboxForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        for article in form.cleaned_data['select']:
            article.state = 1 # Save it
            article.save()
        return saved_articles(request)
    return render(request, 'manage_article_drive/index.html', )