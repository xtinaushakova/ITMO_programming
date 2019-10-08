from util.preprocessing import parse_train_data
from util.preprocessing import get_stats
from util.preprocessing import clean

from util.auxiliary import db_fetch

from collections import defaultdict
from collections import namedtuple

from math import log

import random


def train_test_split(X, y, random_seed=None, train_size=0.7):
    """Перемешать векторы объектов и векторы меток и разделить на тренировочную и тестовую выборки.

    Parameters
    ----------
    X : list
        Вектор объектов News.
    y : list
        Вектор меток.
    random_seed : int
        Зерно для рандомайзера.
    train_size : float
        Доля тренировочной выборки в итоговом наборе.

    Returns
    -------
    tuple
        Кортеж списков, где на четных индексах располагаются
        тренировочные векторы объектов и меток,
        на нечетных - тестовые векторы объектов и меток.

    """
    random.seed(random_seed if random_seed != None else param.SEED)
    batch = list(zip(X, y))
    random.shuffle(batch)

    train = []
    for i in range(round(train_size * len(batch))):
        train.append(batch.pop())

    test = batch
    return ([X_train[0] for X_train in train],
            [y_train[1] for y_train in train],
            [X_test[0] for X_test in test],
            [y_test[1] for y_test in test])


class NaiveBayesClassifier:
    """Наивный Баесовский классификатор, использующий полиномиальную функцию
    распределения,учитывающий проблему Zero Frequency и ликвидирующий риск
    арифметического переполнения снизу.

    Parameters
    ----------
    alpha : float
        Коэффициент сглаживания. По умолчанию 1 - сглаживание Лапласа.

    Attributes
    ----------
    smoothing_factor : float
        Коэффициент сглаживания. По умолчанию 1 - сглаживание Лапласа.

    labels : list
        Список меток.

    train_data : namedtuple
        Именованный кортеж с полями title, authors, domains.
        Каждое поле - словарь с ключами-токенами соответствующей категории и значениями-словарями вида {label: encounters}.

        Пример:
        train_data.title := defaultdict({
            'amazing' : {'-1': 0, '1': 2},
            'fine': {'0': 5, '1': 1},
            ...
        })

    """

    def __init__(self, alpha):
        self.smoothing_factor = alpha

    def fit(self, X, y):
        """Тренировать классификатор относительно вектора объектов X и вектора признаков y.

        Parameters
        ----------
        X : list
            Вектор объектов News.
        y : list
            Вектор меток.

        """
        pool = parse_train_data(X)

        self.labels = list(set(news.label for news in X))
        self.train_data = namedtuple('Train', ['titles', 'authors', 'domains'])
        self.train_data.titles = get_stats(pool['titles'])
        self.train_data.authors = get_stats(pool['authors'])
        self.train_data.domains = get_stats(pool['domains'])

    def predict(self, X):
        """Классифицировать вектор объектов X.

        Parameters
        ----------
        X : list
            Вектор объектов News.

        Returns
        -------
        list
            Список кортежей вида (объект News, (метка, найденная вероятность)).

        Пример:
        predictions := [
            (obj1, ('-1', -12.53)),
            (obj2, ('1', -14.01)),
            ...
        ]
        """
        prediction = []

        for news in X:

            tokens = clean(news.title)
            args = []

            for label in self.labels:

                logged_probabilities = []
                logged_probabilities.append(log(self.prior(label)))

                for token in tokens:
                    logged_probabilities.append(log(self.likelihood(token, label)))

                logged_probabilities.append(log(self.likelihood(news.author, label, mode='author')))

                domain = news.url.split('//')[-1].split('/')[0]
                logged_probabilities.append(log(self.likelihood(domain, label, mode='domain')))

                args.append((label, sum(logged_probabilities)))

            prediction.append((news, max(args, key=lambda x: x[1])))

        return prediction

    def score(self, X_test, y_test):
        """Оценить точность классификатора на тестовой выборке.

        Parameters
        ----------
        X_test : list
            Тестовый вектор размеченных объектов News.
        y_test : list
            Тестовый вектор известных меток.

        Returns
        -------
        float
            Округленная до двух знаков величина - отношение верно классифицированных объектов к общему числу объектов.

        """
        total = 0
        correct = 0
        for i, result in enumerate(self.predict(X_test)):
            if int(result[1][0]) == int(y_test[i]):
                correct += 1
            total += 1
        return round(correct / total, 2)

    def nwords(self, def_dict, label=None):
        """Подсчитать количество слов, вошедших в данный класс (или все классы).

        Parameters
        ----------
        def_dict : defaultdict
            Словарь токенов.
        label : str
            Метка класса. По умолчанию None.

        Returns
        -------
        int / dict
            Количество слов в классе / Словарь классов и соответствующих количеств.

        """
        stat = defaultdict(int)

        for token in def_dict:
            for counts in def_dict[token].items():
                stat[str(counts[0])] += counts[1]

        return stat[label] if label != None else stat

    def likelihood(self, word, label, mode='title'):
        """Правдоподобие.

        Parameters
        ----------
        word : str
            Токен.
        label : str
            Метка.
        mode : str
            Режим, изменяющий категорию в тренировочном наборе.

        Returns
        -------
        float
            Сглаженное (опционально) значение вероятности слова word при условии его принадлежности к label.

        """
        if mode == 'title':
            pool = self.train_data.titles
        elif mode == 'author':
            pool = self.train_data.authors
        elif mode == 'domain':
            pool = self.train_data.domains

        enc_of_this_word = pool[word][label] if pool[word] else 0
        all_words_in_class = self.nwords(pool, label)
        feature_vector_length = len(list(set(word for word in pool)))

        return (enc_of_this_word + self.smoothing_factor) / (all_words_in_class + self.smoothing_factor * feature_vector_length)

    def prior(self, label):
        """Априорная вероятность класса.

        Parameters
        ----------
        label : str
            Метка класса.

        Returns
        -------
        float
            Отношение вхождений класса ко всем классам.

        """
        data = db_fetch(labelled=True)
        batch = list(filter(lambda news: news.label == label, data))
        return len(batch) / len(data)
