import sys
import spotipy
import yaml
import spotipy.util as util
from pprint import pprint
from get_artist import get_song


global sp
global user_config


def load_config():
    global user_config
    stream = open('config.yaml')
    user_config = yaml.load(stream)
    #pprint(user_config)



def get_top_songs_for_artist(artist, song_count=2):
    song_ids = []
    artist_results = sp.search(q='artist:' + artist, type='artist', limit=1)
    #pprint(artist_results)
    print('\n', 'Artist  : ', artist)
    if artist_results['artists']['total']:
        artist_id = artist_results['artists']['items'][0]['id']
        # pprint(artist_id)
        artist_top_tracks = sp.artist_top_tracks(artist_id)
        artist_top_tracks_length = len(artist_top_tracks['tracks'])
        for x in range(0, artist_top_tracks_length if song_count > artist_top_tracks_length else song_count):
                    song_ids.append(artist_top_tracks['tracks'][x]['id'])
                    # pprint(artist_top_tracks['tracks'][x])
                    print('\t', str(len(song_ids)) + ' songs found - ' + artist_top_tracks['tracks'][x]['name'])
    else:
        print('Artist not found - ' + artist)
        # pprint(song_ids)
    return song_ids



def get_top_tracks( artists, top_song_limit_per_artist):

    all_track_ids = []

    for i, current_artist in enumerate(artists):
        api_track_add_limit = 100
        top_artist_songs = get_top_songs_for_artist(current_artist, top_song_limit_per_artist)
        if len(top_artist_songs):
                all_track_ids.extend(top_artist_songs)
        if len(all_track_ids)+ top_song_limit_per_artist > api_track_add_limit or (i == len(artists)-1 and len(all_track_ids)):
                sp.user_playlist_add_tracks(user=user_config['username'], playlist_id=user_config['playlist_id'], tracks=all_track_ids)
                all_track_ids = []



def get_songs_for_artist(artist, track, song_limit_per_artist=5):
    song_ids = []
    #print('artist:' + artist + 'track:' + track)
    track_results = sp.search(q='artist:' + '\"' + artist + '\"' +  'track:' + '\"' + track + '\"', type='track', limit=1)#q='track:' + track, type='track', limit=1)#
    #pprint(track_results)
    print('\t', 'Artist  :  ', artist)
    if track_results['tracks']['total']:
        track_id = track_results['tracks']['items'][0]['id']
        song_ids.append(track_id)
        print('\t', str(len(song_ids)) + ' songs found - ' + track_results['tracks']['items'][0]['name'])
    else:
        print('\t', 'Track not found - ' + track)
        # pprint(song_ids)
    return song_ids


def get_songs_for_artist_album(artist, album, song_count):
    song_ids = []
    #print('artist:' + artist + 'track:' + track)
    album_results = sp.search(q='album:' + '\"'+ album  +'\"' + 'artist:'+ '\"' + artist + '\"', type='album', limit=1)#(q='artist:' + artist + '%20'+  'track:' + track, type='track', limit=1)
    print('\n', 'Artist :  ', artist , '\n', 'Album  :  ', album)
    #pprint(album_results)
    if album_results['albums']['total']:
        album_id = album_results['albums']['items'][0]['id']  
        result = sp.album_tracks(album_id)
        album_tracks_length =  len(result['items'])
        for x in range(0, album_tracks_length if song_count > album_tracks_length else song_count):
            track_id = result['items'][x]['id']
            song_ids.append(track_id)
                    # pprint(artist_top_tracks['tracks'][x])
            print('\t', str(len(song_ids)) + ' songs found - ' + result['items'][x]['name'])
    else:
        print('\t', '- Album not found')
    #pprint(song_ids)
    return song_ids

def get_rym_tracks(artists,album):

    all_track_ids = []

    for i, current_artist in enumerate(artists):
        current_track = album[i]
        api_track_add_limit = 100
        song_limit_per_artist = 1
        artist_songs = get_songs_for_artist(current_artist, current_track, song_limit_per_artist)
        if len(artist_songs):
                all_track_ids.extend(artist_songs)
        if len(all_track_ids)+ song_limit_per_artist > api_track_add_limit or (i == len(artists)-1 and len(all_track_ids)):
                sp.user_playlist_add_tracks(user=user_config['username'], playlist_id=user_config['playlist_id'], tracks=all_track_ids)
                all_track_ids = []


def get_rym_album(artists,album, song_limit_per_album):
    all_track_ids = []

    for i, current_artist in enumerate(artists):
        current_album = album[i]
        api_track_add_limit = 100
        
        artist_songs = get_songs_for_artist_album(current_artist, current_album, song_limit_per_album)
        if len(artist_songs):
                all_track_ids.extend(artist_songs)
        if len(all_track_ids)+ song_limit_per_album > api_track_add_limit or (i == len(artists)-1 and len(all_track_ids)):
                sp.user_playlist_add_tracks(user=user_config['username'], playlist_id=user_config['playlist_id'], tracks=all_track_ids)
                all_track_ids = []

if __name__ == '__main__':
    load_config()

    print('\nType in RYM url: ')
    url = input()

    print('\n\n--- Choose Type --- \n\t(a) Album (n first songs) \n\t(tt) Top Tracks of Artist \n\t(t) Tracks')
    switch = input()

    print('\nType in song limit: ')
    song_limit = input()



    print('Getting songs...')
    album, artist = get_song(url)

    token = util.prompt_for_user_token(user_config['username'], scope='playlist-modify-private,playlist-modify-public', client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if token:
        sp = spotipy.Spotify(auth=token)
        if switch == 'a':
            get_rym_album(artist, album, int(song_limit))
        elif switch == 't':
            get_rym_tracks(artist, album)
        elif switch == 'tt':
            get_top_tracks(artist, int(song_limit))
        else:
            pass
    else:
        print ("Can't get token for", user_config['username'])
