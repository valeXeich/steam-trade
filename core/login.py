import requests

from .db.methods import get_user, set_user_avatar
from .utils import get_avatar_url
from steamlib.models import APIEndpoint

def do_login():
    session = requests.Session()
    user = get_user()
    
    session.cookies.set('browserid', '2468557265578949863')
    session.cookies.set('steamCountry', 'UA%7C24ba0127cdbd4c2483e3e9b1bf881645')
    
    data = {"access_token": user.oauth_token}
    
    tokens = requests.post(
            f"{APIEndpoint.API_URL}IMobileAuthService/GetWGToken/v0001", 
            data=data
        ).json()['response']
    
    for domain in [
            APIEndpoint.STORE_URL[8:-1],
            APIEndpoint.HELP_URL[8:-1],
            APIEndpoint.COMMUNITY_URL[8:-1],
        ]:
            session.cookies.set("birthtime", "-3333", domain=domain)
            session.cookies.set("sessionid", user.session_id, domain=domain)
            session.cookies.set("mobileClientVersion", "0 (2.1.3)", domain=domain)
            session.cookies.set("mobileClient", "android", domain=domain)
            session.cookies.set(
                "steamLogin",
                f"{user.steam_id}%7C%7C{tokens['token']}",
                domain=domain,
            )
            session.cookies.set(
                "steamLoginSecure",
                f"{user.steam_id}%7C%7C{tokens['token_secure']}",
                domain=domain,
                secure=True,
            )
            session.cookies.set("Steam_Language", "english", domain=domain)
    
    avatar_link = get_avatar_url(session)
    if user.avatar != avatar_link:
        set_user_avatar(avatar_link) 
        
    return session
