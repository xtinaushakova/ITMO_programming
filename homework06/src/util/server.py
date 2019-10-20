from util.classifier import NaiveBayesClassifier
from util.classifier import train_test_split

from util.scraping import BASE_URL
from util.scraping import get_news
from util.database import session
from util.database import News

from util.auxiliary import db_fetch

from bottle import route, run, request, template
from bottle import redirect

from sqlalchemy import exists

import util.parameters as param

NUM_PAGES = 1  # Количество страниц, с которых нужно собрать свежие новости.


def start_server():
    """ Обертка для bottle.run(). """
    run(host='localhost', port=8080)


@route('/recommend')
def recommend_page():
    """ Отрендерить страницу с ранжированным списком новостей. """

    data = db_fetch(labelled=True)
    X, y = data, [news.label for news in data]
    X_train, y_train, X_test, y_test = train_test_split(X, y, param.SEED, train_size=param.TRAIN_SIZE)
    classifier = NaiveBayesClassifier(alpha=param.ALPHA)
    classifier.fit(X_train, y_train)

    data = []

    # 1. Получить список неразмеченных новостей из БД
    unlabeled = db_fetch(labelled=False)

    # 2. Получить прогнозы для каждой новости
    for record in classifier.predict(unlabeled):
        data.append((record[0], int(record[1][0]), record[1][1]))  # (News, label, estimation)

    data = sorted(data, key=lambda x: (x[1], x[2]), reverse=True)

    # 3. Вывести ранжированную таблицу с новостями
    return template('templates/recommend.tpl', rows=data)


@route('/')
@route('/classify')
def classify_page():
    """ Отрендерить страницу с классификацией новостей. """
    return template('templates/classify.tpl', rows=db_fetch(labelled=False))


@route('/add_label')
def add_label():
    """ Дать новости отметку в БД. """
    labels = {
        'good': 1,
        'unsure': 0,
        'bad': -1
    }

    try:
        # Получаем значения параметров label и id из GET-запроса.
        # Поскольку при нажатии на категории мы посещаем ссылку вида
        # "/add_label?label=МЕТКА&id=ИДЕНТИФИКАТОР", используем атрибут
        # BaseRequest.query`, чтобы получить доступ к этим данным.
        label = labels[request.query.label] or labels['unsure']
        news_id = request.query.id

        # Получаем запись из БД с соответствующим id.
        s = session()
        news_piece = s.query(News).get(news_id)

        # Меняем значение метки записи на новое значение.
        news_piece.label = label

        # Сохраняем результат в БД.
        s.commit()
    except BaseException:
        pass

    redirect('/classify')


@route('/update_news')
def update_news():
    """ Добавить в БД новую пачку новостей. """
    # 1. Получить данные с новостного сайта
    s = session()
    for piece in get_news(url=BASE_URL + 'newest', n_pages=NUM_PAGES, crawl_delay=30):
        news_piece = News(title=piece['title'],
                             author=piece['author'],
                             url=piece['url'],
                             comments=piece['comments'],
                             points=piece['points'])

        # 2. Проверить, каких новостей еще нет в БД. Будем считать,
        #    что каждая новость может быть уникально идентифицирована
        #    по совокупности двух значений: заголовка и автора
        (piece_exists, ), = s.query(exists().where(News.title == piece['title'] and News.author == piece['author']))

        # 3. Сохранить в БД те новости, которых там нет
        if not piece_exists:
            s.add(news_piece)

        s.commit()
    redirect('/classify')
