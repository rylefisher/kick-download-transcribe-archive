# requirements 
 
- https://handbrake.fr/rotation.php?file=HandBrakeCLI-1.9.2-win-x86_64.zip
- https://github.com/yt-dlp/yt-dlp/releases/download/2025.02.19/yt-dlp.exe
- https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
- https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
- (any firefox version will do but this is what I use) https://portableapps.com/apps/internet/firefox-portable-nightly 

## Howto

Run bat or 
```bat
python venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## prompt to reverse engineer bat

```md
write a bat file that looks for existing venv, if none exists, create venv in working dir. if requirements.txt file found, after activating, pip install upgrade requirements. if main.py file exists in working dir, run, otherwise use set variable py file as backup to run from venv, otherwise use first alphabetic py file. 
```
