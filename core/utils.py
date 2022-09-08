import urllib

from bs4 import BeautifulSoup

def parse(url):
    url = url.split('/')
    name = urllib.parse.unquote(url[6])
    game_id = url[5]
    return name, game_id

def get_avatar_url(session):
    content = session.get('https://store.steampowered.com/').text
    soup = BeautifulSoup(content, 'html.parser')
    link = soup.find('span', {'class': 'pulldown'}).find('img', {'class': 'foryou_avatar'}).attrs['src']
    return f"{link[:-4].replace('akamai', 'cloudflare')}_full.jpg"
