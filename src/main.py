from mutagen.easyid3 import EasyID3
from llama_cpp import Llama
from pathlib import Path
#import re
import os
import json

class music_processor:
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
            self.llm = Llama(config["model_path"], n_ctx=4096, n_threads=6)
            print("model process")
        except:
            self.llm = None

    def extract_and_process(self, file_path):    
        try:
            audio = EasyID3(file_path)
            meta_data = {tag: audio[tag][0] for tag in self.tags if tag in audio}
        except:
            return False

        if not (self.llm and meta_data):
            return False

        try:
            prompt = self.prompt_template.format(metadata={
                "filename": os.path.basename(file_path),
                "metadata": meta_data
            })
            result = self.llm(prompt, max_tokens=1024, temperature=0.7, stream=False)
            if isinstance(result, dict) and 'choices' in result:
                ai_text = result['choices'][0]['text'].strip()
                if ai_text:
                    print(ai_text)
                    print("-"*40)
                    return True
        except:        
            return False
        
        return False

    def run(self):
        mp3_files = list(Path(self.music_folder).glob("*.mp3"))
        if not mp3_files:
            return

        processed = sum(
            self.extract_and_process(str(file_path))
            for file_path in mp3_files
        )
        
        print(f"Processed: {processed}/{len(mp3_files)}")

if __name__ == "__main__":
    music_processor().run()