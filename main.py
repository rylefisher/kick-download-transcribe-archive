# main.py
import required.firefox_linkgrabber as firefox_linkgrabber
import required.log_manager as log_manager
import required.stable_whisper_handler as stable_whisper_handler  # Import Transcriber
import required.ytdlp as ytdlp
import required.transcription_handler as transcription_handler 
import required.file_management as file_management
import required.handbrake_cli as handbrake_cli
import os 

"""
to skip download, use transcription_handler.py
"""

from pathlib import Path

class VODProcessor:
    def __init__(self, channel, firefox_path):
        self.firefox_path = firefox_path  # Initialize the path to Firefox executable
        self.channel = channel
        self.log_manager = log_manager.LogManager(project_name=f"{channel}_VODDownloader")  # Set up log manager
        self.transcriber = stable_whisper_handler.Transcriber(log_manager=self.log_manager)  # Set up transcriber

    def get_vods(self):
        return firefox_linkgrabber.run(self.channel, self.firefox_path)  # Retrieve VODs using Firefox

    def download_vod(self, vod):
        vod_id = vod.split('/')[-1]  # Extract video ID from URL
        download_path = Path(self.log_manager.base_dir) / vod_id  # Create download path
        self.log_manager.log_vod_download(vod)  # Log VOD download attempt
        return ytdlp.download_video(vod, str(download_path))  # Download VOD

    def process_vod(self, file_path):
        cleaned_path = file_management.clean_path(file_path)  # Clean file path
        converter = handbrake_cli.HandbrakeConverter()  # HandBrake conversion setup
        return converter.convert_video(cleaned_path)  # Convert video

    def transcribe_vod(self, vod_path, v_id):
        return transcription_handler.transcribe_video(
            vod_path, v_id
        )  # Get transcription

    def run(self):
        vods = self.get_vods()
        downloaded_vods = self.log_manager.get_downloaded_vods()  # Access downloaded VODs

        for vod in vods:
            downloaded_file = self.download_vod(vod)
            if downloaded_file:
                v_id = vod.split("/")[-1]
                compressed_vod = self.process_vod(downloaded_file)
                transcription = self.transcribe_vod(compressed_vod, v_id)
                if transcription:
                    print(f"Transcription for VOD {v_id}", transcription)
                    break  # Stop after processing the first VOD with transcription

if __name__ == "__main__":
    firefox_executable_path = r"D:\Documents\FirefoxPortable\App\Firefox64\firefox.exe"
    vod_processor = VODProcessor(channel='jstlk', firefox_path=firefox_executable_path)
    vod_processor.run()  # Execute the VOD downloading process
