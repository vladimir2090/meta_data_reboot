from mutagen.easyid3 import EasyID3
from llama_cpp import Llama
from pathlib import Path
#import re
import os
import json

class MusicProcessor:
    __slots__ = ('llm', 'music_folder', 'tags', 'prompt_template', 'chunk_size')

    def __init__(self, config_path: str = "config.json"):
         # read settings from config.json
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.music_folder = config["music_folder"]
        self.tags = tuple(config["tags"])
        self.prompt_template = config["model_promt"]
        self.chunk_size = config["chunk_size"]

        try:
            self.llm = Llama(model_path=config["model_path"], n_ctx=4096, n_threads=6)
            print("Model loaded")
        except Exception as e:
            print(f"Model load failed: {e}")
            self.llm = None

    def extract_and_process(self, file_path):
        try:
            audio = EasyID3(file_path)
            meta_data = {
                tag: audio[tag][0] if tag in audio and audio[tag] else 'N'
                for tag in self.tags
            }
        except Exception as e:
            print(f"[ERROR] Metadata read failed for {file_path}: {e}")
            return False

        if not (self.llm and meta_data):
            return False

        try:
            prompt = self.prompt_template.format(
                filename=os.path.basename(file_path),
                metadata=json.dumps(meta_data, ensure_ascii=False, indent=2)
            )
            result = self.llm(prompt, max_tokens=1024, temperature=0.7, stream=False)

            if isinstance(result, dict) and 'choices' in result:
                ai_text = result['choices'][0]['text'].strip()
                if ai_text:
                    print(f"\n--- {os.path.basename(file_path)} ---\n{ai_text}\n{'-'*40}")
                    return True
        except Exception as e:
            print(f"[ERROR] AI processing failed for {file_path}: {e}")
            return False

        return False

    def run(self):
        mp3_files = list(Path(self.music_folder).glob("*.mp3"))
        if not mp3_files:
            print("No MP3 files found.")
            return

        processed_count = 0
        for file_path in mp3_files:
            if self.extract_and_process(str(file_path)):
                processed_count += 1
        
        print(f"Processed: {processed_count}/{len(mp3_files)}")

if __name__ == "__main__":
    MusicProcessor().run()