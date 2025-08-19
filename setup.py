from setuptools import setup, find_packages

setup(
    name="meta_data_reboot",
    version="1.0.0",
    description="Tool for cleaning and correcting music file names and metadata with local AI",
    author="Vladimir2090",
    author_email="zvladzubkov@gmail.com",
    url="https://github.com/vladimir2090/meta_data_reboot",
    license="GPLv3",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Topic :: Multimedia :: Sound/Audio",
    "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    packages=find_packages(),
    install_requires=[
        "mutagen",
        "llama_cpp"
    ],
    python_requires=">=3.9",
    entry_points={
    "console_scripts": [
        "meta-reboot=meta_data_reboot.main:main",
    ],
},
)