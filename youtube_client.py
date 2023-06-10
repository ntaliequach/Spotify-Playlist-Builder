import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl


class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title
        
class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track

class YouTubeClient(object):        # methods interact with YT data API
    def __init__(self, credentials_location):
        SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
        #disable oathlib's https verification when running locally 
        #do not leave this option enabled in production
        
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
        api_service_name = "youtube"
        api_version = "v3"
        CLIENT_SECRETS_FILE = 'creds/client_secret.json'
    
    
    #get credentials and create API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )
        
        self.youtube_client = youtube

    
    
    def get_playlists(self):
        request = self.youtube_client.playlist().list(
            part = "id, snippet",
            maxResults = 50,
            mine = True
        )
        response = request.execute()
    
        #list of playlists, response dictionary, key items
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]
    
        return playlists
    
    
    def get_videos_from_playlist(self, playlist_id):
        
        songs = []
        
        request = self.youtube_client.playlistItems().list(
            playlsitId = playlist_id,
            part = "id, snippet" 
        )
        
        response = request.execute()
        
        #get data from each video
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist, track = self.get_artist_and_track(video_id)
            if artist and track:
                songs.append(Song(artist, track))
                
        return songs
    
    def get_artist_and_track(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        #avoid output logs
        video = youtube_dl.YoutubeDL({'quiet':True}).extract_info(
            youtube_url, download=False
        )
        
        artist = video['artist']
        track = video['track']
        
        return artist, track