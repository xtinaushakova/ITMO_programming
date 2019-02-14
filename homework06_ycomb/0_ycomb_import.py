import requests 
from bs4 import BeautifulSoup

r = requests.get("https://news.ycombinator.com/newest")