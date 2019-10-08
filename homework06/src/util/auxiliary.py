from util.scraping import BASE_URL
from util.scraping import get_news
from util.database import session
from util.database import News


def db_fetch(labelled):
    s = session()
    if labelled:
        return s.query(News).filter(News.label != None).all()
    else:
        return s.query(News).filter(News.label == None).all()


def collect_base_training_samples():
    """Произвести сбор ~1000 свежих новостей с 34 страниц.
    Используется для сбора тренировочных данных для классификатора.
    """
    s = session()
    for piece in get_news(url=BASE_URL+'newest', n_pages=34, crawl_delay=30):
        news = News(title=piece['title'],
                    author=piece['author'],
                    url=piece['url'],
                    comments=piece['comments'],
                    points=piece['points'])
        s.add(news)
        s.commit()
