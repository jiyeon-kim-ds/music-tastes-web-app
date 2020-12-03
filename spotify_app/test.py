
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8a196cb7c2ea43f389b42ef106cf480e",
                                                           client_secret="8ef2c43b00694216bb86e4e191b80c22"))
# results = sp.search(q='weezer', type='artist')
# items = results['artists']['items']
# if len(items) > 0:
#     artist_info = items[0]
# else:
#     pass

# artist_id = artist_info['id']
# top_tracks = sp.artist_top_tracks(artist_id, country='US')
# first_track = top_tracks["tracks"]
# first_track = first_track[0]
# first_track_id = first_track["id"]
# features = sp.audio_features(f'spotify:track{first_track_id}')
# features = features[0]

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

results = sp.search(q='artist:' + 'BTS', type='artist')
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
print(first_track_id)
print('--------')
og_features = sp.audio_features(first_track_id)
features = og_features[0]

print(og_features)
print('--------')
print(features)
into_df(features)
print(df.head())




# top tracks
"""
dict = {
    "tracks": [
        {
            "album": {
                "album_type": "album",
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/3jOstUTkEu2JkjvRdBA5Gu"
                        },
                        "href": "https://api.spotify.com/v1/artists/3jOstUTkEu2JkjvRdBA5Gu",
                        "id": "3jOstUTkEu2JkjvRdBA5Gu",
                        "name": "Weezer",
                        "type": "artist",
                        "uri": "spotify:artist:3jOstUTkEu2JkjvRdBA5Gu"
                    }
                ],
                "external_urls": {
                    "spotify": "https://open.spotify.com/album/2OBSz5Nlto0Q5CtYPzPY7c"
                },
                "href": "https://api.spotify.com/v1/albums/2OBSz5Nlto0Q5CtYPzPY7c",
                "id": "2OBSz5Nlto0Q5CtYPzPY7c",
                "images": [
                    {
                        "height": 640,
                        "url": "https://i.scdn.co/image/ab67616d0000b2731e0dc5baaabda304b0ad1815",
                        "width": 640
                    },
                    {
                        "height": 300,
                        "url": "https://i.scdn.co/image/ab67616d00001e021e0dc5baaabda304b0ad1815",
                        "width": 300
                    },
                    {
                        "height": 64,
                        "url": "https://i.scdn.co/image/ab67616d000048511e0dc5baaabda304b0ad1815",
                        "width": 64
                    }
                ],
                "name": "Weezer (Green Album)",
                "release_date": "2001-05-15",
                "release_date_precision": "day",
                "total_tracks": 10,
                "type": "album",
                "uri": "spotify:album:2OBSz5Nlto0Q5CtYPzPY7c"
            },
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/3jOstUTkEu2JkjvRdBA5Gu"
                    },
                    "href": "https://api.spotify.com/v1/artists/3jOstUTkEu2JkjvRdBA5Gu",
                    "id": "3jOstUTkEu2JkjvRdBA5Gu",
                    "name": "Weezer",
                    "type": "artist",
                    "uri": "spotify:artist:3jOstUTkEu2JkjvRdBA5Gu"
                }
            ],
            "available_markets": [],
            "disc_number": 1,
            "duration_ms": 200306,
            "explicit": false,
            "external_ids": {
                "isrc": "USIR10110358"
            },
            "external_urls": {
                "spotify": "https://open.spotify.com/track/2MLHyLy5z5l5YRp7momlgw"
            },
            "href": "https://api.spotify.com/v1/tracks/2MLHyLy5z5l5YRp7momlgw",
            "id": "2MLHyLy5z5l5YRp7momlgw",
            "is_local": false,
            "is_playable": true,
            "name": "Island In The Sun",
            "popularity": 76,
            "preview_url": null,
            "track_number": 4,
            "type": "track",
            "uri": "spotify:track:2MLHyLy5z5l5YRp7momlgw"
        },
"""