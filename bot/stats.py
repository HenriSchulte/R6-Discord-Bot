import requests
from bs4 import BeautifulSoup


class Player:
    def __init__(self, name, rank, mmr):
        self.name = name
        self.rank = rank
        self.mmr = mmr


def get_user_page(username):
    url = f'https://r6.tracker.network/profile/pc/{username}/'
    return requests.get(url=url)


def parse_page_content(page_text):
    soup = BeautifulSoup(page_text, 'html.parser')
    mmr_div = soup.find('div', class_='trn-scont__aside')
    content_div = mmr_div.find('div', class_='trn-card__content')
    content = content_div.contents[3].contents[3].contents[1]
    rank = content.contents[1].string
    mmr = content.contents[3].string
    return rank, mmr


def get_player_stats(username):
    response = get_user_page(username)
    try:
        rank, mmr = parse_page_content(response.text)
        player = Player(username, rank, mmr)
    except:
        player = Player(username, 'Not found', '')
    return player