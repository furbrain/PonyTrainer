import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PonyTrainer",
    author="Phil Underwood",
    author_email="beardydoc@gmail.com",
    description="Companion program for the Shetland Attack Pony 5",
    long_description=long_description,
    url="https://github.com/furbrain/PonyTrainer",
    packages=["src"],
    scripts=["src/PonyTrainer.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        'Operating System :: Microsoft :: Windows',
    ],
)
