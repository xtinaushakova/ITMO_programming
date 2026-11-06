# Dependencies

Use Python 3.12+; `.python-version` replaces the deprecated Python 3.6 Heroku runtime declaration. Create a virtual environment, upgrade pip and install `requirements.txt`.

Requests and its transport dependencies are updated to corrected versions. PyTelegramBotAPI is updated for compatibility with current Python. The redundant `bs4` alias and third-party `datetime` package are removed; use `beautifulsoup4` and Python's standard-library `datetime`.

Run `python -m unittest discover -s tests -v` from this directory. Tests use fixture HTML, a stub config and a mocked Telegram transport, with no live requests or messages. Production startup still requires valid existing configuration and credentials.
