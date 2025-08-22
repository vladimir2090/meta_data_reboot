from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from llama_cpp import Llama
from pathlib import Path
import shutil
import os
import re
import json
import atexit

class MusicProcessor:
    __slots__ = ('llm', 'music_folder', 'music_recode_folder', 'tags', 'system_prompt', 'rename_format', 'chunk_size', "stopwords", "remove_images")

    def __init__(self, config_path: str = "config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.music_folder = config["music_folder"]
        self.music_recode_folder = config["music_recode_folder"]
        self.tags = tuple(config["tags"])
        self.system_prompt = config["system_prompt"]
        self.rename_format = config["rename_format"]
        self.chunk_size = config["chunk_size"]
        self.stopwords = tuple(config["stopwords"])
        self.remove_images = config["remove_images"]

        try:
            self.llm = Llama(
                model_path=config["model_path"],
                n_ctx=4096,
                n_threads=os.cpu_count() or 4
            )
            atexit.register(self._cleanup_llm)
            print("Model loaded")
        except Exception as e:
            print(f"[ERROR] Model load failed: {e}")
            self.llm = None

        os.makedirs(self.music_recode_folder, exist_ok=True)

    def _cleanup_llm(self):
        if hasattr(self, 'llm') and self.llm is not None:
            try:
                self.llm.close()
            except:
                pass

    def clean_stopwords(self, text: str) -> str:
        if not text or text == "N":
            return text
        cleaned = text
        for word in self.stopwords:
            pattern = re.compile(rf"(?<!\w){re.escape(word)}(?!\w)", flags=re.IGNORECASE)
            cleaned = pattern.sub("", cleaned)
        cleaned = " ".join(cleaned.split())
        return cleaned if cleaned else "N"
    
    def extract_metadata(self, file_path):
        try:
            audio = EasyID3(file_path)
            metadata = {
                tag: audio[tag][0] if tag in audio and audio[tag] and audio[tag][0].strip() else 'N'
                for tag in self.tags
            }

            cleaned_metadata = {k: self.clean_stopwords(v) for k, v in metadata.items()}
            filename = os.path.basename(file_path)
            cleaned_filename = self.clean_stopwords(filename)
            
            return {"filename": filename, "cleaned_filename": cleaned_filename, "metadata": cleaned_metadata}
        except Exception as e:
            print(f"[SKIP] Corrupted file {file_path}: {e}")
            return None

    def process_batch(self, batch):
        if not self.llm or not batch:
            return None

        files_data_json = json.dumps(batch, ensure_ascii=False, indent=2)
        prompt = f"{self.system_prompt}\n\n{files_data_json}"
        try:
            result = self.llm(
                f"[INST]\n{prompt}\n[/INST]",
                max_tokens=1024,         
                temperature=0.6,
                top_p=0.9,
                top_k=50,
                min_p=0.05,
                repeat_penalty=1.1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stream=False,
                stop=[],
                seed=0
            )

            if isinstance(result, dict) and 'choices' in result:
                ai_text = result['choices'][0]['text'].strip()
                raw = result['choices'][0]['text']
                print("FULL RESULT:", result)
                with open("debug_ai_response.txt", "w", encoding="utf-8") as f:
                    f.write(raw)
                return self.parse_ai_response(ai_text)
        except Exception as e:
            print(f"[ERROR] AI processing failed: {e}")
            return None

    def parse_ai_response(self, ai_text: str):
        try:
            return json.loads(ai_text)
        except:
            match = re.search(r'\[.*\]', ai_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            return None

    def apply_changes(self, file_path, new_name, new_metadata):
        try:
            temp_path = Path(self.music_recode_folder) / Path(file_path).name
            shutil.copy2(file_path, temp_path)

            final_path = Path(self.music_recode_folder) / new_name

            audio = MP3(temp_path, ID3=EasyID3)
            for tag, value in new_metadata.items():
                if not value or value.strip() == "":
                    value = "N"
                audio[tag] = value

            if self.remove_images:
                id3_tags = ID3(temp_path)
                apic_keys = [key for key in id3_tags.keys() if key.startswith('APIC')]
                for key in apic_keys:
                    del id3_tags[key]
                if apic_keys:
                    id3_tags.save()

            audio.save()

            if temp_path != final_path:
                os.rename(temp_path, final_path)

            print(f"[OK] {Path(file_path).name} -> {final_path.name}")
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
            print(ai_output)
            if not ai_output:
                continue

            for old_data, new_data in zip(batch, ai_output):
                old_file = Path(self.music_folder) / old_data["filename"]
                try:
                    metadata = new_data.get("metadata", {})
                    required_fields = ["artist", "title", "album"]
                    
                    safe_metadata = {}
                    for field in required_fields:
                        safe_metadata[field] = metadata.get(field, "Unknown")
                    
                    new_file_name = self.rename_format.format(**safe_metadata)
                    print(new_file_name)
                except (KeyError, ValueError) as e:
                    print(f"[WARNING] Filename format error: {e}, using original name")
                    new_file_name = old_data["filename"]

                if self.apply_changes(old_file, new_file_name, new_data["metadata"]):
                    processed_count += 1

        print(f"Processed: {processed_count}/{len(mp3_files)}")

def main():
    MusicProcessor().run()

if __name__ == "__main__":
    main()