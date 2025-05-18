import requests
from bs4 import BeautifulSoup
from .models import Author, Quote, Tag
from django.contrib.auth.models import User

BASE_URL = 'http://quotes.toscrape.com'

def scrape_quotes(user):
    """
    Скрейпить цитати з quotes.toscrape.com і зберігає у БД.
    user - користувач, який буде вказаний як created_by для цитат.
    """
    page_url = '/page/1/'

    while page_url:
        url = BASE_URL + page_url
        print(f"Scraping {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')

        for quote_block in quotes:
            text = quote_block.find('span', class_='text').get_text(strip=True)
            author_name = quote_block.find('small', class_='author').get_text(strip=True)
            author_link = quote_block.find('a')['href']

            author, created = Author.objects.get_or_create(full_name=author_name)
            if created:
                author_details_url = BASE_URL + author_link
                author_resp = requests.get(author_details_url)
                author_soup = BeautifulSoup(author_resp.text, 'html.parser')
                born_date = author_soup.find('span', class_='author-born-date').text.strip()
                born_location = author_soup.find('span', class_='author-born-location').text.strip()
                description = author_soup.find('div', class_='author-description').text.strip()
                author.born_date = born_date
                author.born_location = born_location
                author.description = description
                author.save()

            tag_elements = quote_block.find_all('a', class_='tag')
            tags = []
            for tag_el in tag_elements:
                tag_name = tag_el.text.strip()
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)

            quote_obj, created = Quote.objects.get_or_create(
                quote=text,
                author=author,
                created_by=user,
            )
            if created:
                quote_obj.tags.set(tags)
                quote_obj.save()

        next_button = soup.find('li', class_='next')
        if next_button:
            page_url = next_button.find('a')['href']
        else:
            page_url = None

    print("Scraping finished.")
