from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Author, Quote, Tag
from .forms import RegisterForm, AuthorForm, QuoteForm
from .scrape import scrape_quotes

def index(request):
    quotes_list = Quote.objects.all().order_by('-id')
    paginator = Paginator(quotes_list, 10)  # 10 цитат на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Найпопулярніші теги (top 10)
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]

    context = {
        'page_obj': page_obj,
        'top_tags': top_tags,
    }
    return render(request, 'quotes_app/index.html', context)


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    quotes = Quote.objects.filter(author=author)

    context = {
        'author': author,
        'quotes': quotes,
    }
    return render(request, 'quotes_app/author_detail.html', context)


def quote_detail(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, 'quotes_app/quote_detail.html', {'quote': quote})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматичний вхід після реєстрації
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'quotes_app/register.html', {'form': form})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AuthorForm()
    return render(request, 'quotes_app/add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.created_by = request.user
            quote.save()
            form.save_m2m()  # Для тегів
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'quotes_app/add_quote.html', {'form': form})


def quotes_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes_list = Quote.objects.filter(tags=tag).order_by('-id')

    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'quotes_app/quotes_by_tag.html', context)


@user_passes_test(lambda u: u.is_superuser)
def scrape_view(request):
    scrape_quotes(request.user)
    return redirect('index')
