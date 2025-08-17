from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from llama_cpp import Llama
from pathlib import Path
import shutil
import os
import json

class MusicProcessor:
    __slots__ = ('llm', 'music_folder', 'music_recode_folder', 'tags', 'system_prompt', 'rename_format', 'chunk_size', "STOPWORDS")

    def __init__(self, config_path: str = "config.json"):
        # read settings from config.json
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.music_folder = config["music_folder"]
        self.music_recode_folder = config["music_recode_folder"]
        self.tags = tuple(config["tags"])
        self.system_prompt = config["system_prompt"]
        self.rename_format = config["rename_format"]
        self.chunk_size = config["chunk_size"]
        self.STOPWORDS = config["STOPWORDS"]

        try:
            self.llm = Llama(
                model_path=config["model_path"],
                n_ctx=4096,
                n_threads=os.cpu_count() or 4
            )
            print("Model loaded")
        except Exception as e:
            print(f"[ERROR] Model load failed: {e}")
            self.llm = None

        os.makedirs(self.music_recode_folder, exist_ok=True)

    def extract_metadata(self, file_path):
        try:
            audio = EasyID3(file_path)
            return {
                "filename": os.path.basename(file_path),
                "metadata": {
                    tag: audio[tag][0] if tag in audio and audio[tag] else 'N'
                    for tag in self.tags
                }
            }
        except Exception as e:
            print(f"[ERROR] Metadata read failed for {file_path}: {e}")
            return None

    def process_batch(self, batch):
        if not self.llm or not batch:
            return None

        files_data_json = json.dumps(batch, ensure_ascii=False, indent=2)
        prompt = f"{self.system_prompt}\n\n{files_data_json}"
        try:
            result = self.llm(
                prompt,
                max_tokens=2048,
                temperature=0.7,
                stream=False
            )

            if isinstance(result, dict) and 'choices' in result:
                ai_text = result['choices'][0]['text'].strip()

                try:
                    return json.loads(ai_text)
                except json.JSONDecodeError:
                    print(f"[ERROR] Failed to parse AI JSON output:\n{ai_text[:200]}...")
                    return None
        except Exception as e:
            print(f"[ERROR] AI processing failed: {e}")
            return None

    def apply_changes(self, file_path, new_name, new_metadata):
        try:
            new_path = Path(self.music_recode_folder) / new_name
            shutil.copy2(file_path, new_path)

            audio = MP3(new_path, ID3=EasyID3)
            for tag, value in new_metadata.items():
                if value and value != "N":
                    audio[tag] = value
            audio.save()

            print(f"[OK] {os.path.basename(file_path)} -> {new_name}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to apply changes for {file_path}: {e}")
            return False

    def run(self):
        mp3_files = list(Path(self.music_folder).glob("*.mp3"))
        if not mp3_files:
            print("No MP3 files found.")
            return

        metadata_list = []
        for file_path in mp3_files:
            data = self.extract_metadata(str(file_path))
            if data:
                metadata_list.append(data)

        processed_count = 0
        for i in range(0, len(metadata_list), self.chunk_size):
            batch = metadata_list[i:i + self.chunk_size]
            ai_output = self.process_batch(batch)
            if not ai_output:
                continue

            for old_data, new_data in zip(batch, ai_output):
                old_file = Path(self.music_folder) / old_data["filename"]

                try:
                    new_file_name = self.rename_format.format(**new_data["metadata"])
                except KeyError:
                    new_file_name = old_data["filename"]

                if self.apply_changes(old_file, new_file_name, new_data["metadata"]):
                    processed_count += 1

        print(f"Processed: {processed_count}/{len(mp3_files)}")

def main():
    MusicProcessor().run()

if __name__ == "__main__":
    main()