from mutagen.easyid3 import EasyID3
from llama_cpp import Llama
import os
import re
import shutil
import json

# read settings from config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

llm = None
try:
    llm = Llama(config["model_path"], n_ctx=4096, n_threads=6)
    print("model process")
except Exception as error:
    print(f"error model isn't process: {error}")

def get_music_meta_data(file_path):
    try:      
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

def ai_recoding(metadata):
    global llm
    if not llm:
        print("model isn't working")
        return {}
    
    try:
        prompt = config["model_promt"].format(metadata=str(metadata))
        result = llm(prompt, max_tokens=1024, temperature=0.7)
        return result
    except Exception as error:
        print(f'Error: {error}')
        return{}

def process_chunks(files_chunk):
    for entry in files_chunk:
        print(f"Processing: {entry.path}")

        metadata = get_music_meta_data(entry.path)

        if metadata:
            ai_result = ai_recoding(metadata)
            if ai_result:
                print(ai_result)
                print("-" * 40)

def main():
    try:
        mp3_files = []
        for entry in os.scandir(config["music_folder"]):
            if entry.is_file() and entry.name.lower().endswith(".mp3"):
                mp3_files.append(entry)
        print(f"found {len(mp3_files)} mp3 files")

        chunk_size = config.get("chunk_size", 10)

        for i in range(0, len(mp3_files), chunk_size):
            chunk = mp3_files[i:i + chunk_size]
            print(i//chunk_size + 1, len(chunk))
            process_chunks(chunk)
                
    except Exception as error:
        print(f'Error: {error}')

if __name__ == "__main__":
    main()