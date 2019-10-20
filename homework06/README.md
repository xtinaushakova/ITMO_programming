# Наивный Баесовский классификатор для ранжирования новостной ленты сайта HackerNews.

> ### TODO
> - [x] Улучшить структуру  проекта
> - [x] **СБАЛАНСИРОВАТЬ ДАТАСЕТ** (**овер**семплинг)
> Приводит к переобучению
> - [ ] **СБАЛАНСИРОВАТЬ ДАТАСЕТ** (стратифицированной выборкой)
> - [ ] Исправить парадокс точности
> - [ ] [Пофиксить](https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185) импорты из src/tests/test_score.py
> - [ ] Использовать ```numpy``` для ускорения вычислений
> - [ ] Добавить разбиение текста на биграммы
> - [ ] Добавить учет токенизированного текста статей из ссылок
> - [ ] Попробовать TF-IDF метрику?
> - [ ] Добавить логирование в функциях модулей src/util/server.py, src/util/scraping.py и других

## Установка зависимостей

```pip install -r requirements.txt```

```python -m nltk.downloader 'punkt'```

## Запуск

Локальный сервер

```python3 main.py```

Бенчмарк классификатора

```python3 test_score.py```

## Демо

### Классификация
![alt text](https://github.com/antoniugov/hackernews-classifier/blob/dev/images/classify.png "Classification demo")

### Ранжирование
![alt text](https://github.com/antoniugov/hackernews-classifier/blob/dev/images/recommend.png "Recommendation demo")
