# log_manager.py
import os
import json
from pathlib import Path

class LogManager:
    def __init__(self, project_name="MyProject"):
        self.base_dir = Path.home() / "Documents" / project_name
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.vod_log_file = self.base_dir / "downloaded_vods.json"
        self.transcription_log_file = self.base_dir / "vod_transcriptions.json"
        self._init_log_file(self.vod_log_file)
        self._init_log_file(self.transcription_log_file)

    def _init_log_file(self, file_path):
        if not file_path.exists():
            with open(file_path, "w") as f:
                json.dump([], f)

    def log_vod_download(self, vod_info):
        vods = self.get_downloaded_vods()
        vods.append(vod_info)
        with open(self.vod_log_file, "w") as f:
            json.dump(vods, f, indent=4)

    def get_downloaded_vods(self):
        with open(self.vod_log_file, "r") as f:
            return json.load(f)

    def log_transcription(self, vod_id, transcription):
        transcriptions = self.get_transcriptions()
        transcriptions[vod_id] = transcription
        with open(self.transcription_log_file, "w") as f:
            json.dump(transcriptions, f, indent=4)

    def get_transcriptions(self):
        # Retrieve transcriptions
        with open(self.transcription_log_file, "r") as f:
            return json.load(f)
    def filter_vods(self, vods, downloaded_vods):
        return [vod for vod in vods if vod["id"] not in downloaded_vods]
