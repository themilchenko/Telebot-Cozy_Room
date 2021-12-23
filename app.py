#!/usr/bin/python3

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, json, render_template
import time
import config

# App config
app = Flask(__name__)

app.secret_key = 'SOMETHING-RANDOM'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

@app.route('/')
def login():    
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/getTracks")

@app.route('/logout')
def logout():
    shutdown_server()
    return "Go back."

def shutdown_server():
    URL = os.path.realpath(os.path.dirname(__file__))
    URLString = URL + '/is_finished.txt'
    with  open(URLString, 'w') as file:
        file.write('1')

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/getTracks')
def get_all_tracks():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    me = sp.current_user()

    # получаю топ артистов за разные промежутки времени
    top_artists_l = sp.current_user_top_artists(limit=10, offset=0, time_range="long_term")
    top_artists_m = sp.current_user_top_artists(limit=10, offset=0, time_range="medium_term")
    top_artists_s = sp.current_user_top_artists(limit=10, offset=0, time_range="short_term")

    # получаю топ песен за разные промежутки времени
    top_tracks_l = sp.current_user_top_tracks(limit=10, offset=0, time_range="long_term")
    top_tracks_m = sp.current_user_top_tracks(limit=10, offset=0, time_range="medium_term")
    top_tracks_s = sp.current_user_top_tracks(limit=10, offset=0, time_range="short_term")

    genres = sp.recommendation_genre_seeds()

    JSON_URL = os.path.realpath(os.path.dirname(__file__))

    URLString = JSON_URL + '/json_files/me.json'
    with  open(URLString, 'w') as file:
        json.dump(me, file, ensure_ascii=False, indent=4)  

    URLString = JSON_URL + '/json_files/top_artists_s.json'
    with  open(URLString, 'w') as file:
        json.dump(top_artists_s, file, ensure_ascii=False, indent=4)
    URLString = JSON_URL + '/json_files/top_artists_m.json'
    with  open(URLString, 'w') as file:
        json.dump(top_artists_m, file, ensure_ascii=False, indent=4)
    URLString = JSON_URL + '/json_files/top_artists_l.json'
    with  open(URLString, 'w') as file:
        json.dump(top_artists_l, file, ensure_ascii=False, indent=4)

    URLString = JSON_URL + '/json_files/top_tracks_s.json'
    with  open(URLString, 'w') as file:
        json.dump(top_tracks_s, file, ensure_ascii=False, indent=4)
    URLString = JSON_URL + '/json_files/top_tracks_m.json'
    with  open(URLString, 'w') as file:
        json.dump(top_tracks_m, file, ensure_ascii=False, indent=4)
    URLString = JSON_URL + '/json_files/top_tracks_l.json'
    with  open(URLString, 'w') as file:
        json.dump(top_tracks_l, file, ensure_ascii=False, indent=4)

    URLString = JSON_URL + '/json_files/genres.json'
    with  open(URLString, 'w') as file:
        json.dump(genres, file, ensure_ascii=False, indent=4)        

    return redirect("/logout")


def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="135f8f328b9e4e869dc15d378310a727",
            client_secret="04e0627e34694eb8a8da84f703381893",
            redirect_uri=url_for('authorize', _external=True),
            scope="user-top-read")      


if __name__ == "__main__":
    app.run()
