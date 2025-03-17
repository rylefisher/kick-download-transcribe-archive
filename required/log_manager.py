import os
import json
from pathlib import Path


class LogManager:

    def __init__(self, project_name="MyProject"):
        self.base_dir = Path.home() / "Documents" / project_name
        self.transcripts_dir = Path.home() / "Documents" / project_name  / 'transcripts'
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        self.vod_log_file = self.base_dir / "downloaded_vods.json"
        self.transcription_log_file = self.base_dir / "vod_transcriptions.json"
        self._init_log_file(self.vod_log_file)
        self._init_log_file(self.transcription_log_file)

    def _init_log_file(self, file_path):
        # Ensure the file exists and initialize it if it doesn't
        if not file_path.exists():
            with open(file_path, "w") as f:
                json.dump([], f)

    def log_vod_download(self, vod_info):
        # Log the downloaded VOD information
        vods = self.get_downloaded_vods()
        vods.append(vod_info)
        with open(self.vod_log_file, "w") as f:
            json.dump(vods, f, indent=4)

    def get_downloaded_vods(self):
        # Retrieve the list of downloaded VODs
        with open(self.vod_log_file, "r") as f:
            return json.load(f)

    def log_transcription(self, vod_id, transcription):
        # Log the transcription with VOD ID
        transcriptions = self.get_transcriptions()
        transcriptions[vod_id] = transcription
        with open(self.transcription_log_file, "w") as f:
            json.dump(transcriptions, f, indent=4)

    def get_transcriptions(self):
        # Retrieve the transcription list
        with open(self.transcription_log_file, "r") as f:
            return json.load(f)

    def update_vod_log_with_url(self, url):
        # Update log with the given URL
        vods = self.get_downloaded_vods()
        if url not in vods:
            vods.append(url)
            with open(self.vod_log_file, "w") as f:
                json.dump(vods, f, indent=4)

    def filter_undownloaded_vods(self, vod_urls):
        # Return URLs that have not been downloaded yet
        downloaded_vods = self.get_downloaded_vods()
        return [url for url in vod_urls if url not in downloaded_vods]
