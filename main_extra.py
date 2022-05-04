import re
import bs4
import requests
from heads import HEADERS
import time

HUBS = ['Python *', 'Процессоры', 'Usability *', 'Laravel *']
# HUBS = ['дизайн', 'фото', 'web', 'python']
url_main = 'https://habr.com'
url_next = 'https://habr.com'
no_article = True
pattern = r'анали\w+'
pattern_c = re.compile(pattern)


def get_cur_page(soup_page):
    page_current = soup_page.find('span', class_='tm-pagination__page tm-pagination__page_current').text
    return page_current.strip()


def get_next_link(soup_page):
    pages_href = soup_page.find_all('div', class_='tm-pagination')
    page_next_href = ''
    link_next = ''
    for page_href in pages_href:
        page_next_href = page_href.find('a', id='pagination-next-page').attrs['href']
    if page_next_href != '':
        link_next = url_main + page_next_href
        time.sleep(0.2)
    return link_next


if __name__ == '__main__':
    n = 0
    while n < 7:
        response = requests.get(url=url_next, headers=HEADERS)
        response.raise_for_status()
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all('article')
        for article in articles:
            hubs = article.find_all(class_='tm-article-snippet__hubs-item')
            hubs = set(hub.text.strip() for hub in hubs)
            for hub in hubs:
                if hub in HUBS:
                    no_article = False
                    date_ = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
                    href = article.find(class_='tm-article-snippet__title-link').attrs['href']
                    link = url_main + href
                    title = article.find('h2').find('span').text
                    result = f"Дата публикации - {date_}, статья - {title} доступна по ссылке - {link}"
                    print(result)
                    response = requests.get(link, headers=HEADERS)
                    len_list = len(pattern_c.findall(response.text))
                    print(f'количество слов {pattern} на странице {get_cur_page(soup)}: {len_list}\n')
        url_next = get_next_link(soup)

        if url_next == '':
            break
        n = n + 1

    if no_article:
        print(f"Не найдено ни одной статьи по ключевым полям: {', '.join(HUBS)}")
