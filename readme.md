# meta_data_reboot

A Python script for modifying file metadata using AI assistance with ease and flexibility.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Development Status](https://img.shields.io/badge/status-60%25%20complete-green.svg)

## 🚧 Development Status

⚠️ **Progress Update!** This program has made significant progress (approximately 60% complete). Core functionality is working, but some features are still in development. Use with caution!

## 📝 Description

**meta_data_reboot** is a Python utility that combines metadata extraction with AI-powered processing to help users analyze and modify file metadata intelligently. The tool uses local AI models to process metadata and suggest improvements.

## 🎯 Current Features

✅ **MP3 Metadata Parser** - Extract metadata from MP3 files using mutagen library  
✅ **AI Model Integration** - Process metadata using local Llama models  
✅ **Chunk Processing** - Handle large batches of files efficiently  
✅ **Error Handling** - Basic error logging and exception management  
✅ **Configuration System** - JSON-based configuration for flexibility  

## 📋 TODO List

- [x] **Parser implementation** - ✅ Core functionality to read and extract metadata from MP3 files
- [x] **config.json file** - ✅ Configuration system for model settings, tags, and processing parameters
- [x] **Data model integration** - ✅ Send and process metadata through AI model with chunked processing
- [x] **Basic error handling** - ✅ Exception management and error logging implemented
- [ ] **Modified file creation** - Generate new files with updated metadata based on AI suggestions
- [ ] **Cross-platform installation** - Simple installation scripts for Windows, macOS, and Linux

## 🔧 What's Currently Working

Based on the current codebase:

**Metadata Extraction**: The parser successfully extracts metadata from MP3 files including:
- Artist, Album, Title, Date, Genre and other configurable tags
- Uses mutagen.easyid3 for reliable MP3 metadata handling

**AI Processing**: 
- Integration with Llama.cpp for local AI model processing
- Configurable prompts for metadata analysis
- Chunked processing to handle large music libraries efficiently

**Configuration Management**:
- JSON-based config for model paths, processing settings, and metadata tags
- Flexible chunk size configuration for batch processing

**Error Handling**:
- Try-catch blocks for file processing errors
- Model loading error management
- Graceful handling of missing or corrupted metadata

## 🛠️ Installation & Setup

1. git clone https://github.com/yourusername/meta_data_reboot.git
2. cd meta_data_reboot
3. pip install mutagen, llama-cpp-python, json
4. recomend: pip install shutil

## 💡 Usage

*Usage examples and documentation will be provided as development progresses.*

## 🤝 Contributing

**Help is greatly appreciated!** This project is created by a beginner developer who is learning and growing. Whether you're an experienced programmer or just starting out, your contributions are welcome.

Ways you can help:
- Report bugs and issues
- Suggest new features
- Contribute code improvements
- Help with documentation
- Share feedback and ideas

Feel free to open issues or submit pull requests. Every contribution, no matter how small, makes a difference!

## 📄 License

**meta_data_reboot** is distributed under the GNU General Public License v3.0. This means you can freely use, modify, and share this program, as long as you keep the same license for any work based on it.

See the [LICENSE](LICENSE) file for full details.

## 👨‍💻 Author

Created with ❤️ by a passionate beginner developer learning Python and exploring the world of file management tools.

---

*This project is actively under development. Star ⭐ this repository to stay updated on progress!*