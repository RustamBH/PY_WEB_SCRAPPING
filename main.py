import bs4
import requests
from heads import HEADERS

HUBS = ['Python *', 'Процессоры', 'Usability *', 'Laravel *']
# HUBS = ['дизайн', 'фото', 'web', 'python']
url = 'https://habr.com'

response = requests.get(url=url, headers=HEADERS)
response.raise_for_status()
text = response.text
soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')

no_article = True
for article in articles:
    hubs = article.find_all(class_='tm-article-snippet__hubs-item')
    hubs = set(hub.text.strip() for hub in hubs)
    for hub in hubs:
        if hub in HUBS:
            no_article = False
            date_ = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            link = url + href
            title = article.find('h2').find('span').text
            result = f"Дата публикации - {date_}, статья - {title} доступна по ссылке - {link}"
            print(result)

if no_article:
    print(f"Не найдено ни одной статьи по ключевым полям: {', '.join(HUBS)}")