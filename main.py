# main.py
import firefox_linkgrabber
from log_manager import LogManager
from transcriber import Transcriber  # Import Transcriber

FIREFOX = r"C:\Users\dower\Documents\FirefoxPortable\App\Firefox64\firefox.exe"

def main():
    # Initialize LogManager
    log_manager = LogManager(project_name="VODDownloader")
    # Initialize Transcriber
    transcriber = Transcriber(log_manager=log_manager)
    vods = firefox_linkgrabber(FIREFOX)

    # Get already downloaded VODs
    downloaded_vods = log_manager.get_downloaded_vods()
    downloaded_vod_ids = {vod["id"] for vod in downloaded_vods}

    # Filter VODs
    vods_to_download = log_manager.filter_vods(vods, downloaded_vod_ids)

    for vod in vods_to_download:
        # Log downloaded VOD
        log_manager.log_vod_download(vod)

        # Transcribe the video and log the transcription
        video_file_path = (
            f"downloads/{vod['id']}.mp4"  # Assume videos are saved in downloads folder
        )
        transcription = transcriber.transcribe_video(video_file_path, vod["id"])

        if transcription:
            print(f"Transcription for VOD {vod['title']}", transcription)


if __name__ == "__main__":
    main()
