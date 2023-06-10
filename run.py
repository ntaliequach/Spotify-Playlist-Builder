import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from spotify_client import SpotifyClient
from youtube_client import YouTubeClient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow




def run():
    #1 get a list of our playlists from YT
    youtube_client = YouTubeClient('./creds/client_secret.json')
    spotify_client = SpotifyClient(os.getenv('SPOTIFY_AUTH_TOKEN'))
    playlists = youtube_client.get_playlists()
    
    #2 ask which playlist we want to get the music videos from
    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")
    
    #3 for each video in the playlist get the song info from YT
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)}")
    
    #4 search for songs on Spotify
    for song in songs:
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song:
                print(f"Added {song.artist}")
    
    
    
    
    
if __name__ == '__main__':
    run()