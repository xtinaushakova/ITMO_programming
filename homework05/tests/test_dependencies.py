"""Check HTTP and Telegram compatibility without sending messages."""
import json
import unittest
from unittest.mock import patch

import requests
import telebot
import sys
from pathlib import Path
from types import ModuleType
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class DependencySmokeTests(unittest.TestCase):
    def test_telegram_send_through_mocked_requests_transport(self):
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps({'ok': True, 'result': {
            'message_id': 1, 'date': 0,
            'chat': {'id': 123, 'type': 'private'}, 'text': 'test'
        }}).encode()
        with patch.object(requests.sessions.Session, 'request', return_value=response) as transport:
            message = telebot.TeleBot('123456:TEST_TOKEN_FOR_OFFLINE_TEST').send_message(123, 'test')
        self.assertEqual(message.text, 'test')
        transport.assert_called_once()

    def test_schedule_html_parser(self):
        config = ModuleType('config')
        config.domain = 'https://example.invalid'
        with patch.dict(sys.modules, {'config': config}):
            import schedule_parser
        html = '<table id="1day"><tr><td class="time"><span>08:20-09:50</span></td><td class="room"><span>101</span><dd>Main</dd></td><td class="lesson">Math</td></tr></table>'
        self.assertEqual(schedule_parser.parse_schedule_for_a_day(html, '1'),
                         (['08:20-09:50'], ['101, Main'], ['Math']))
        self.assertIsNone(schedule_parser.parse_schedule_for_a_day(html, '2'))


if __name__ == '__main__':
    unittest.main()
