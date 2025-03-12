import required.firefox_linkgrabber as firefox_linkgrabber
import required.log_manager as log_manager
import required.stable_whisper_handler as stable_whisper_handler
import required.ytdlp as ytdlp
import required.transcription_handler as transcription_handler
import required.file_management as file_management
import required.handbrake_cli as handbrake_cli
from pathlib import Path


class VODProcessor:
    def __init__(self, channel, firefox_path):
        self.firefox_path = firefox_path
        self.channel = channel
        self.log_manager = log_manager.LogManager(
            project_name=f"{channel}_VODDownloader"
        )
        self.transcriber = stable_whisper_handler.Transcriber(
            log_manager=self.log_manager
        )

    def get_vods(self, headless=True):
        # Retrieve VODs using the Firefox link grabber
        return firefox_linkgrabber.run(self.channel, self.firefox_path, headless)

    def download_vod(self, vod):
        # Download VOD and log the download
        vod_id = vod.split("/")[-1]
        download_path = Path(self.log_manager.base_dir) / vod_id
        self.log_manager.log_vod_download(vod)
        return ytdlp.download_video(vod, str(download_path))

    def process_vod(self, file_path):
        # Clean file path and convert video using Handbrake CLI
        cleaned_path = file_management.clean_path(file_path)
        converter = handbrake_cli.HandbrakeConverter()
        return converter.convert_video(cleaned_path)

    def transcribe_vod(self, vod_path, v_id):
        # Transcribe video and return transcription
        return transcription_handler.transcribe_video(vod_path, v_id)

    def run(self, only_lastest=True):
        # Process VODs, downloading and transcribing each
        vods = self.get_vods()
        downloaded_vods = self.log_manager.get_downloaded_vods()
        undownloaded_vods = self.log_manager.filter_undownloaded_vods(vods)
        for vod in undownloaded_vods:
            downloaded_file = self.download_vod(vod)
            if downloaded_file:
                v_id = vod.split("/")[-1]
                compressed_vod = self.process_vod(downloaded_file)
                transcription = self.transcribe_vod(compressed_vod, v_id)
                if transcription:
                    print(f"Transcription for VOD {v_id}", transcription)
                if only_lastest:
                    break


if __name__ == "__main__":
    firefox_executable_path = r"D:\Documents\FirefoxPortable\App\Firefox64\firefox.exe"
    vod_processor = VODProcessor(channel="jstlk", firefox_path=firefox_executable_path)
    vod_processor.run()
