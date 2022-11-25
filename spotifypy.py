import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os 

def getTrackNames(sp, playlist_link):
    
    if not playlist_link:
        playlist_link = 'https://open.spotify.com/playlist/55LlnKooyeoItHwENCAKpI?si=301fc0b042594b07'

    try:
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]

        results = sp.playlist_tracks(playlist_URI)

        playlist_name = sp.user_playlist(user=None, playlist_id=playlist_URI, fields="name")
        playlist_desc = sp.user_playlist(user=None, playlist_id=playlist_URI, fields="description")

        user = results["items"][0]["added_by"]["external_urls"]["spotify"].split("/")[-1].split("?")[0]

        user_name = sp.user(user=user)["display_name"]

        print(f"Parsing songs from '{playlist_name['name']}' by {user_name}...")
        

        track_list = results["items"]
        songs = []
        tag_list = []

        while results['next']:
            results = sp.next(results)
            track_list.extend(results['items'])

        num = 1
        for track in track_list:
            song = track["track"]["name"] + " by " + track["track"]["artists"][0]["name"]
            songs.append(song)
            tags = {}

            tags["num"] = num
            tags["title"] = track["track"]["name"]
            tags["artist"] = track["track"]["artists"][0]["name"]
            tags["album"] = track["track"]["album"]["name"]
            tags["date created"] = track["track"]["album"]["release_date"]
            tags["artwork_url"] = track["track"]["album"]["images"][0]['url']
            tags["year"] = track["track"]["album"]["release_date"].split('-')[0]
            
            tag_list.append(tags)

            for k,v in track["track"].items():
                print(k, " - ", v)

            '''albumm = sp.album(track["album"]["external_urls"]["spotify"])["genres"]
            print(albumm["genres"])'''

            print()
            num += 1
            
        playlist_length = len(track_list)
        
        #print(playlist_name["name"], playlist_desc["description"], songs, playlist_length, tag_list)
        return playlist_name["name"], playlist_desc["description"], songs, playlist_length, tag_list
    
    except Exception as e:
        print(e)        
        print("Invalid url or private playlist")

def main(URL):
    SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET= os.environ["SPOTIPY_CLIENT_SECRET"]
    
    CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

    playlist_url = URL
    if playlist_url == "":
        playlist_url = None

    return getTrackNames(sp, playlist_url)
    

#main("https://open.spotify.com/playlist/1LhCSJoaMdlAZgh16Yhcmi?si=88b259b656854033")