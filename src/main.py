from mutagen.easyid3 import EasyID3
import os
#import re
import json

# read settings from config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

def get_music_meta_data(file_path):
    try:
        if not os.path.exists(file_path): #you can delete this
            print(f'File not found {file_path}')
            return {}
        
        audio = EasyID3(file_path)
  
        meta_data = {   #dict with tags
            tag: audio.get(tag, ['N'])[0]  # no data
            for tag in config["tags"]
            if tag in audio
        }
        
        return meta_data
        
    except Exception as error:
        print(f'Error: {error}')
        return {}

def main():
    try:
    # go all mp3 in the folder
        for file_name in os.listdir(config["music_folder"]):
            if file_name.lower().endswith(".mp3"):
                print(f"Processing: {os.path.join(config['music_folder'], file_name)}")

                # read and write meta_data
                metadata = get_music_meta_data(os.path.join(config["music_folder"], file_name))  # directly pass path
                for key, value in metadata.items():
                    print(f"{key}: {value}")

    except Exception as error:
        print(f'Error: {error}')

if __name__ == "__main__":
    main()
