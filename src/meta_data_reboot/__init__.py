from .main import MusicProcessor, main

__all__ = ["MusicProcessor", "main"]
__version__ = "0.9.1"

def info():
    return f"meta_data_reboot v{__version__} — Music metadata processor with AI."