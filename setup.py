from setuptools import setup, find_packages

setup(
    name="meta_data_reboot",
    version="0.9.1",
    description="A Python script for modifying file name and metadata using local AI assistance",
    author="Vladimir2090",
    url="https://github.com/vladimir2090/meta_data_reboot",
    packages=find_packages(),
    install_requires=[
        "mutagen",
        "llama_cpp"
    ],
    python_requires=">=3.9",
)