"""Offline integration checks for the supported dependency versions."""
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from wsgiref.util import setup_testing_defaults

SOURCE = Path(__file__).resolve().parents[1] / 'src'
sys.path.insert(0, str(SOURCE))


class DependencySmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.previous_cwd = Path.cwd()
        cls.directory = tempfile.TemporaryDirectory()
        os.chdir(cls.directory.name)
        Path('data').mkdir()
        from util import server, database
        import bottle
        bottle.TEMPLATE_PATH.insert(0, str(SOURCE))
        cls.app = bottle.default_app()
        cls.database = database

    @classmethod
    def tearDownClass(cls):
        cls.database.engine.dispose()
        os.chdir(cls.previous_cwd)
        cls.directory.cleanup()

    def request(self, path, query=''):
        environ = {}
        setup_testing_defaults(environ)
        environ.update(SERVER_PROTOCOL='HTTP/1.1', PATH_INFO=path, QUERY_STRING=query, **{'wsgi.input': io.BytesIO()})
        status = []
        body = b''.join(self.app(environ, lambda s, h, exc_info=None: status.append(s)))
        return status[0], body

    def test_database_and_bottle_routes(self):
        db = self.database
        with db.session() as session:
            news = db.News(title='Python news', author='tester', url='https://example.com', points=1, comments=0)
            session.add(news)
            session.commit()
            news_id = news.id
        status, body = self.request('/classify')
        self.assertTrue(status.startswith('200'), body)
        self.assertIn(b'Python news', body)
        status, body = self.request('/add_label', f'label=good&id={news_id}')
        self.assertTrue(status.startswith('303'), body)
        with db.session() as session:
            self.assertEqual(session.get(db.News, news_id).label, '1')

    def test_nltk_and_classifier_without_model_downloads(self):
        from util.preprocessing import clean
        from util.classifier import NaiveBayesClassifier
        from types import SimpleNamespace
        self.assertIn('run', clean('Running Python!'))
        rows = [SimpleNamespace(title='Python code', author='a', url='https://a.example', label='1'),
                SimpleNamespace(title='Spam ads', author='b', url='https://b.example', label='-1')]
        classifier = NaiveBayesClassifier(alpha=1)
        classifier.fit(rows, ['1', '-1'])
        with patch.object(classifier, 'prior', return_value=0.5):
            self.assertEqual(classifier.predict([rows[0]])[0][1][0], '1')

    def test_updated_html_parser(self):
        from bs4 import BeautifulSoup
        from util.scraping import extract_news
        from types import SimpleNamespace
        self.assertEqual(BeautifulSoup('<p class="story">News</p>', 'html.parser').select_one('.story').text, 'News')
        # An empty legacy news table still parses without a live HTTP request.
        html = '<table><tr><td><table></table><table><tr></tr><tr></tr></table></td></tr></table>'
        with patch('util.scraping.requests.get', return_value=SimpleNamespace(text=html)):
            self.assertEqual(extract_news('https://example.invalid'), [])


if __name__ == '__main__':
    unittest.main()
