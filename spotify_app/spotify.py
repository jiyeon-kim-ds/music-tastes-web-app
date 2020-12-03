import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import json
import pickle 
import pandas as pd
from sqlalchemy import update
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
import psycopg2
import urllib.parse as up
load_dotenv()

DATABASE = os.getenv('DATABASE_URI')
FILEPATH = './models/spotify_model.pkl'
app = Flask(__name__)
engine = create_engine(DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
FILEPATH = os.path.join(os.path.dirname(__file__), "models",
                          "spotify_model.pkl")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8a196cb7c2ea43f389b42ef106cf480e",
                                                           client_secret="8ef2c43b00694216bb86e4e191b80c22"))

# results = sp.search(q='Red Velvet', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])


class artist(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    loveorhate = db.Column(db.String)


def get_artists():
    # return artist.query.all()
    return db.session.query(artist).all()

def into_df(track):
    danceability = []
    energy = []
    key = []
    loudness = []
    speechiness = []
    mode = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []

    danceability.append(track['danceability'])
    energy.append(track['energy'])
    key.append(track['key'])
    loudness.append(track['loudness'])
    speechiness.append(track['speechiness'])
    acousticness.append(track['acousticness'])
    instrumentalness.append(track['instrumentalness'])
    liveness.append(track['liveness'])
    valence.append(track['tempo'])
    mode.append(track['mode'])
    tempo.append(track['tempo'])  

    feature_dict = {
    'danceability' : danceability,
    'energy' : energy,
    'key' : key,
    'loudness' : loudness,
    'mode' : mode,
    'speechiness' : speechiness,
    'acousticness' :  acousticness,
    'instrumentalness' : instrumentalness,
    'liveness' : liveness,
    'valence' : valence,
    'tempo' : tempo
    }
    df = pd.DataFrame(feature_dict)
    return df




@app.route('/')
def index():
    data = get_artists()
    print('--------------------------')
    print(data)
    return render_template('index.html', data=data)    

@app.route('/add', methods=["GET", "POST"])
def add_artist(artist_name=None):
    if request.method == "POST":
        print(dict(request.form))
        result = request.form
        results = sp.search(q='artist:' + result['artist_name'], type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist_info = items[0]
        else:
                return None
        new_artist = artist(id = artist_info['id'], name = artist_info['name'], loveorhate = "NA")
        # db.session.add(new_artist)
        # # db.session.commit()
        db.session.add(new_artist)
        db.session.commit()
    
    # results = sp.search(q='artist:' + artist_name, type='artist')
    # items = results['artists']['items']
    # if len(items) > 0:
    #     artist_info = items[0]
    # else:
    #         return None
    # new_artist = artist(id = artist_info['id'], name = artist_name)
    return render_template('add.html')

@app.route('/delete', methods=["GET", "POST"])
def delete_artist(artist_name=None):
    if request.method == "POST":
        print(dict(request.form))
        result = request.form
        artist_name = result['artist_name']
        artist.query.filter_by(name=artist_name).delete()
        print(artist_name)
        print('아티스트 삭제')
        # db.session.delete(artist)
        db.session.commit()

    return render_template('delete.html')


@app.route('/analyze')
def analyze_artists(artist_name=None):
    return render_template('analyze.html')

@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == "POST":
        print(dict(request.form))
        result = request.form
        artist_name = result['artist_name']
        results = sp.search(q='artist:' + artist_name, type='artist')
        items = results['artists']['items']

        if len(items) > 0:
            artist_info = items[0]
        else:
            pass

        artist_id = artist_info['id']
        top_tracks = sp.artist_top_tracks(artist_id, country='US')
        first_track = top_tracks["tracks"]
        first_track = first_track[0]
        first_track_id = first_track["id"]
        og_features = sp.audio_features(first_track_id)
        features = og_features[0]
        # breakpoint()
        df = into_df(features)

        # model import
        with open(FILEPATH, 'rb') as model_file:
            model = pickle.load(model_file)
        print("Model Loaded")
        print()
        pred_id = model.predict(df)
        print(f"The final prediction value is {pred_id}")
        pred_id = pred_id[0]
        print(pred_id)
        if pred_id == 1:
            pred_id = 'I will love it'
            artist_update = artist(id=artist_id)
            # artist_update.loveorhate = pred_id
            db.session.query(artist).filter(artist.id == artist_id).update({'loveorhate': pred_id})
            db.session.commit()
        elif pred_id == 0:
            # pred_id = 'I will hate it'
            db.session.query(artist).filter(artist.id == artist_id).update({'loveorhate': pred_id})
            # artist_update.loveorhate = pred_id
            db.session.commit()
        return pred_id
        # result_update = update(artist).where(artist.id==artist_id).values(loveorhate=pred_id)
        # db.session.add(result_update)
        # to_update = db.session.query(artist).filter(artist.id == artist_id).one()
        # to_update.loveorhate = pred_id
        # db.session.query(artist).filter(artist.id==artist_id).update({'loveorhate':pred_id},synchronize_session='fetch')
        db.session.query(artist).filter(artist.id == artist_id).update({'loveorhate': pred_id})
        db.session.commit()
    return render_template('result.html', result=pred_id)

if __name__ == "__main__":
    app.run(debug=True)
