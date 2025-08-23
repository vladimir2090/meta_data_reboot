from .main import MusicProcessor, main

__all__ = ["MusicProcessor", "main"]
__version__ = "1.0.0"

def info():
    return f"metadata-reboot v{__version__} — Music metadata processor with AI."