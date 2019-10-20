# import nltk
# nltk.download()

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize

from collections import defaultdict

import util.parameters as param

import string


def clean(text):
    """Произвести токенизацию и очистку строки текста.

    Parameters
    ----------
    text : str
        Текст.
    remove_stopwords : bool
        Удалять ли стоп-слова из текста.

    Returns
    -------
    list
        Список токенов.

    """
    # Разбиваем заголовок на слова.
    tokens = [token.lower() for token in word_tokenize(text)]

    # Отделяем от каждого слова пунктуацию.
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # Удаляем отделенные знаки пунктуации.
    words = [word for word in stripped if word.isalpha()]

    if not param.PRESERVE_STOP_WORDS:
        # Убираем шумовые слова (стоп-слова).
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if w not in stop_words]

    if param.TOKEN_CLEANING_MODE == 'stemming':
        # Используем стеммер Портера, чтобы отсечь у слов окончания и суффиксы.
        porter = PorterStemmer()
        cleaned = [porter.stem(word) for word in words]
    elif param.TOKEN_CLEANING_MODE == 'lemmatization':
        # В качестве альтернативы можем использовать лемматайзер WordNet.
        wordnet_lemmatizer = WordNetLemmatizer()
        cleaned = [wordnet_lemmatizer.lemmatize(word) for word in words]

    # Оставим лишь уникальные слова, чтобы избежать искажения в вычислении вероятностей.
    cleaned = list(set(cleaned))

    return cleaned


def get_stats(pool):
    """Собрать статистику вхождений токенов в классы.

    Parameters
    ----------
    pool : list
        Список кортежей вида (label, token).

    Returns
    -------
    defaultdict
        Словарь с ключами-токенами и значениями-словарями вида {label: encounters}

        Пример:
        {
            'amazing' : {'-1': 0, '1': 2},
            'fine': {'0': 5, '1': 1},
            ...
        }

    """
    stats = defaultdict(lambda: defaultdict(int))

    for entry in pool:
        stats[entry[1]][entry[0]] += 1

    return stats


def parse_train_data(X):
    """Парсит вектор объектов News, формируя пул токенов в трех разных категориях:
    'titles'  : токены из заголовкв постов
    'authors' : никнеймы авторов постов
    'domains' : домены исходныъ ссылок, на которые ведет пост

    Parameters
    ----------
    X : list
        Вектор объектов News.

    Returns
    -------
    dict
        Словарь с ключами-категорими токенов и значениями-списками кортежей вида (label, token)

        Пример:
        {
            'titles' : {
                ('-1', 'politics'),
                ('-1', 'finance'),
                ('0', 'startup'),
                ('1', 'ai'),
                ('1', 'cv'),
                ('1', 'gaming'),
                ...
            },
            'authors' : {
                ('-1', 'saruman_theNaughty'),
                ('-1', 'Xx_legolas69_xX'),
                ('1', 'frodo12'),
                ('1', 'galadriel_1400'),
                ...
            },
            'domains' : {
                ('-1', 'www.shittyarticles.com'),
                ('1', 'www.researchgate.com'),
                ('0', 'www.zen.yandex.ru'),
                ('1', 'www.medium.com'),
                ...
            },
            ...
        }

    """
    pool = {'titles': [], 'authors': [], 'domains': []}

    for record in X:
        label, author, title, url = record.label, record.author, clean(record.title), record.url
        domain = url.split('//')[-1].split('/')[0]
        pool['titles'].extend([(label, word) for word in title])
        pool['authors'].extend([(label, author)])
        pool['domains'].extend([(label, domain)])

    return pool
