from __future__ import print_function
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
from pprint import pprint
import time
import sys
import pandas as pd
import os
import pickle
from sklearn.linear_model import LogisticRegression
MODEL_FILE = os.path.join(os.path.dirname(__file__), "models",
                          "spotify.pkl")

# 사실은 내 플레이리스트를 옮기는 파일

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8a196cb7c2ea43f389b42ef106cf480e",
                                                           client_secret="8ef2c43b00694216bb86e4e191b80c22"))
playlist_id = 'spotify:user:spotifycharts:playlist:4AO1VfWZ8PXDFvelNkr7OU'
# results = sp.playlist_tracks(playlist_id, limit=2)

results = sp.playlist_tracks(playlist_id, limit = 100)
result = json.dumps(results, indent=4)
info = results["items"]
# print(json.dumps(info[1], indent=4))
artists = []
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

for i in range(len(info)):
    # 딕셔너리에서 아티스트명만 빼내 리스트로 전환
    song = info[i]
    artist_info = song["track"]["album"]["artists"]
    artist_info = artist_info[0]
    artist_name = artist_info["name"]
    artists.append(artist_name)
    song_id = song["track"]["id"]
    song_name = song["track"]["name"]
    song_uri = song["track"]["uri"]
    features = sp.audio_features(f'spotify:track:{song_uri}')
    features = features[0]

    # features to list
    danceability.append(features['danceability'])
    energy.append(features['energy'])
    key.append(features['key'])
    loudness.append(features['loudness'])
    speechiness.append(features['speechiness'])
    acousticness.append(features['acousticness'])
    instrumentalness.append(features['instrumentalness'])
    liveness.append(features['liveness'])
    valence.append(features['tempo'])
    mode.append(features['mode'])
    tempo.append(features['tempo'])

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
# 선호가수 df
like_df = pd.DataFrame(feature_dict)
like_df['y'] = 1
# 선호하지 않는 가수 df

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
def dislike(song_uri):
    features_dislike = sp.audio_features(f'spotify:track:{song_uri}')
    features_dislike = features_dislike[0]
    danceability.append(features_dislike['danceability'])
    energy.append(features_dislike['energy'])
    key.append(features_dislike['key'])
    loudness.append(features_dislike['loudness'])
    speechiness.append(features_dislike['speechiness'])
    acousticness.append(features_dislike['acousticness'])
    instrumentalness.append(features_dislike['instrumentalness'])
    liveness.append(features_dislike['liveness'])
    valence.append(features_dislike['tempo'])
    mode.append(features_dislike['mode'])
    tempo.append(features_dislike['tempo'])


dislike('6MFRtRMQWObCVWE4TC1Pbu')
dislike('2Z8yfpFX0ZMavHkcIeHiO1')
dislike('0VjIjW4GlUZAMYd2vXMi3b')
dislike('1tkg4EHVoqnhR6iFEXb60y')
dislike('0GzuHFG4Ql6DoyxFRnIk3F')
dislike('6HlE9t71z9DjGi7KqSyEpA')


feature_dislike = {
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
dislike_df = pd.DataFrame(feature_dislike)
dislike_df['y'] = 0



df = pd.concat([like_df, dislike_df])
print(df.head())

"""
features    
[{'danceability': 0.544, 'energy': 0.718, 'key': 5, 'loudness': -8.286, 'mode': 0, 'speechiness': 0.24, 'acousticness': 0.0996, 'instrumentalness': 0, 'liveness': 0.2, 'valence': 0.361, 'tempo': 80.095, 'type': 'audio_features', 'id': '3NnINnjKVVs03xat0qLQFx', 'uri': 'spotify:track:3NnINnjKVVs03xat0qLQFx', 'track_href': 'https://api.spotify.com/v1/tracks/3NnINnjKVVs03xat0qLQFx', 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/3NnINnjKVVs03xat0qLQFx', 'duration_ms': 118466, 'time_signature': 3}]
"""
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "spotify_model.pkl")


def train_model():
    logistic = LogisticRegression()
    X = df.drop(['y'], axis=1)
    y = df['y']
    logistic.fit(X, y)
    return logistic

    
def save_model(model):
    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)



def load_model():

    with open(MODEL_FILE, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
        print("Model Loaded")

    return loaded_model


def load_model():
    with open(MODEL_PATH, "rb") as file:
        loaded_model = pickle.load(file)
    return loaded_model


if __name__ == "__main__":
    # 모델을 훈련하고 저장
    trained_model = train_model()
    save_model(trained_model)
    
    # 저장된 모델 불러오기
    # loaded_model = load_model()


# dict = {
#     "added_at": "2020-04-28T06:38:01Z",
#     "added_by": {
#         "external_urls": {
#             "spotify": "https://open.spotify.com/user/jiyeon.kim.1991"
#         },
#         "href": "https://api.spotify.com/v1/users/jiyeon.kim.1991",
#         "id": "jiyeon.kim.1991",
#         "type": "user",
#         "uri": "spotify:user:jiyeon.kim.1991"
#     },
#     "is_local": false,
#     "primary_color": null,
#     "track": {
#         "album": {
#             "album_type": "single",
#             "artists": [
#                 {
#                     "external_urls": {
#                         "spotify": "https://open.spotify.com/artist/4V8LLVI7PbaPR0K2TGSxFF"
#                     },
#                     "href": "https://api.spotify.com/v1/artists/4V8LLVI7PbaPR0K2TGSxFF",
#                     "id": "4V8LLVI7PbaPR0K2TGSxFF",
#                     "name": "Tyler, The Creator",
#                     "type": "artist",
#                     "uri": "spotify:artist:4V8LLVI7PbaPR0K2TGSxFF"
#                 }
#             ],
#             "external_urls": {
#                 "spotify": "https://open.spotify.com/album/5ufhf4tUkvX78Y8nJgXlqw"
#             },
#             "href": "https://api.spotify.com/v1/albums/5ufhf4tUkvX78Y8nJgXlqw",
#             "id": "5ufhf4tUkvX78Y8nJgXlqw",
#             "images": [
#                 {
#                     "height": 640,
#                     "url": "https://i.scdn.co/image/ab67616d0000b27314018bd9158a07c9a6a58f54",
#                     "width": 640
#                 },
#                 {
#                     "height": 300,
#                     "url": "https://i.scdn.co/image/ab67616d00001e0214018bd9158a07c9a6a58f54",
#                     "width": 300
#                 },
#                 {
#                     "height": 64,
#                     "url": "https://i.scdn.co/image/ab67616d0000485114018bd9158a07c9a6a58f54",
#                     "width": 64
#                 }
#             ],
#             "name": "GROUP B",
#             "release_date": "2020-01-25",
#             "release_date_precision": "day",
#             "total_tracks": 1,
#             "type": "album",
#             "uri": "spotify:album:5ufhf4tUkvX78Y8nJgXlqw"
#         },
#         "artists": [
#             {
#                 "external_urls": {
#                     "spotify": "https://open.spotify.com/artist/4V8LLVI7PbaPR0K2TGSxFF"
#                 },
#                 "href": "https://api.spotify.com/v1/artists/4V8LLVI7PbaPR0K2TGSxFF",
#                 "id": "4V8LLVI7PbaPR0K2TGSxFF",
#                 "name": "Tyler, The Creator",
#                 "type": "artist",
#                 "uri": "spotify:artist:4V8LLVI7PbaPR0K2TGSxFF"
#             }
#         ],
#         "disc_number": 1,
#         "duration_ms": 118466,
#         "episode": false,
#         "explicit": true,
#         "external_ids": {
#             "isrc": "USQX92000077"
#         },
#         "external_urls": {
#             "spotify": "https://open.spotify.com/track/3NnINnjKVVs03xat0qLQFx"
#         },
#         "href": "https://api.spotify.com/v1/tracks/3NnINnjKVVs03xat0qLQFx",
#         "id": "3NnINnjKVVs03xat0qLQFx",
#         "is_local": false,
#         "name": "GROUP B",
#         "popularity": 59,
#         "preview_url": "https://p.scdn.co/mp3-preview/b303830d8a366281d6b461d02ab1c9a3cfad5dd9?cid=8a196cb7c2ea43f389b42ef106cf480e",
#         "track": true,
#         "track_number": 1,
#         "type": "track",
#         "uri": "spotify:track:3NnINnjKVVs03xat0qLQFx"
#     },
#     "video_thumbnail": {
#         "url": null
#     }
# }