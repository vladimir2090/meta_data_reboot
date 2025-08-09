from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
#import re
import os


def get_music_meta_data(file_path):
    music_tags = ['title', 'artist', 'album', 'date', 'genre', 'tracknumber', 'albumartist']
    
    try:
        audio = EasyID3(file_path)
        mp3_info = MP3(file_path)

        if not os.path.exists(file_path):
            print(f'File not found {file_path}')
            return {}
        
        meta_data = {
            tag: audio.get(tag, ['N (no data)'])[0]
            for tag in music_tags
            if tag in audio
        }
        
        return meta_data
        
    except Exception as error:
        print(f'Error: {error}')
        return {}


def main():
    try:
        file_path = r"C:\Users\admin\Desktop\music_noformat\2mashi_-_bosaya_(zaycev.net)-1.mp3"
        
        metadata = get_music_meta_data(file_path)
        
        for key, value in metadata.items():
            print(f"{key}: {value}")

    except Exception as error:
        print(f'Error: {error}')

if __name__ == "__main__":
    main()