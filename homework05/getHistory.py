from collections import Counter
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple
from api import get_message_history

from api import messages_get_history
from api_models import Message
from config import config

Dates = List[datetime.date]
Frequencies = List[int]

plotly.tools.set_credentials_file(
    username=config['plotly_username'],
    api_key=config['plotly_api_key']
)

def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> list:
    dates = []
    for message in messages:
        dates.append(message['date'])
    for i in range(len(dates)):
        dates[i] = datetime.datetime.fromtimestamp(dates[i]).strftime('%Y-%m-%d')
    if dates:
        return dates


def plotly_messages_freq(dates: list) -> None:
    a = Counter(dates)
    x = list(a.keys())
    y = list(a.values())
    data = [go.Scatter(x=x,y=y)]
    py.iplot(data)

if __name__ == '__main__':
    plotly_messages_freq(count_dates_from_messages(get_message_history(user_id)))
