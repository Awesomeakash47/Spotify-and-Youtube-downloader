from pytube import YouTube
from pytube import Playlist
from pytube import Search
import os
import spotifypy
from moviepy.editor import *
import eyed3
import urllib.request



def downloader(video, folder_dir, p_length, c, song_details=None):
    st = video.streams.get_by_itag(140)

    if song_details == None:
        st.download(output_path=folder_dir)
    else:
        st.download(output_path=folder_dir, filename=song_details[c-1]['title'])

    print(f'downloaded ({c}/{p_length}) - {video.title} ')


def converter(folder_dir):
    os.chdir(folder_dir)
    folder = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)

    for video in folder:
        base, ext = os.path.splitext(video)

        clip = AudioFileClip(folder_dir + "\\" + video)
        clip.write_audiofile(folder_dir+"\\"+base+".mp3")
        clip.close()
        os.remove(folder_dir + "\\" + video)

def tagger(folder_dir, song_details):
    os.chdir(folder_dir)
    folder = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)

    for c, audio in enumerate(folder):
        audiofile = eyed3.load(folder_dir + "\\" + audio)
        tags = song_details[c]

        response = urllib.request.urlopen(tags["artwork_url"])  
        imagedata = response.read()

        audiofile.tag.track_num = tags["num"]
        audiofile.tag.artist = tags["artist"]
        audiofile.tag.album = tags["album"]
        audiofile.tag.title = tags["title"]

        for i in range(7):
            audiofile.tag.images.set(i, imagedata , "image/jpeg")

        audiofile.tag.save()
    print("Tags created")

def YTdownloader(URL):
    p = Playlist(URL)
    print(f"downloading from {p.title}")

    for c, url in enumerate(p.video_urls):
        video = YouTube(url)
        folder_dir = os.path.dirname(__file__)+"\\"+p.title

        downloader(video, folder_dir, p.length, c+1)
     
        '''if c > 2:
            break'''

    print(f"\nConverting all to mp3")
    converter(folder_dir)
    print("conversion finished")

def SPdownloader(URL):
    playlist = spotifypy.main(URL)
    songName_list = playlist[2]
    folder_dir = os.path.dirname(__file__)+"\\"+playlist[0]
    p_length = playlist[3]
    song_details = playlist[4]


    for c, songName in enumerate(songName_list):
        s = Search(songName+ " lyrics")

        for video in s.results:
            downloader(video, folder_dir, p_length, c+1, song_details)
            break
        
        '''if c > 10:
            break'''

    print(f"\nConverting all to mp3")
    converter(folder_dir)
    tagger(folder_dir, song_details)
    print("conversion finished")

def main():
    URL = input("\nEnter Youtube or Spotify playlist to download: ")

    try:
        if "youtube" in URL:
            YTdownloader(URL)
        elif "spotify" in URL:
            SPdownloader(URL)
        else:
            print("Enter a valid link")
            main()
    except Exception as e:
        print("some glitch... script will be restarting")
        print(e)
        main()

if __name__ == "__main__":
    main()