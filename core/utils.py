import urllib

def parse(url):
    url = url.split('/')
    name = urllib.parse.unquote(url[6])
    game_id = url[5]
    return name, game_id
