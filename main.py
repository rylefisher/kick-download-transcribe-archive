# main.py
import firefox_linkgrabber
import log_manager
import transcriber  # Import Transcriber

FIREFOX = r"D:\Documents\FirefoxPortable\App\Firefox64\firefox.exe"

def main():
    # Initialize LogManager
    log_manager_ = log_manager.LogManager(project_name="VODDownloader")
    # Initialize Transcriber
    transcriber_ = transcriber.Transcriber(log_manager=log_manager_)
    vods = firefox_linkgrabber.SeleniumFetcher.main(FIREFOX)

    # Get already downloaded VODs
    downloaded_vods = log_manager_.get_downloaded_vods()
    downloaded_vod_ids = {vod["id"] for vod in downloaded_vods}

    # Filter VODs
    vods_to_download = log_manager_.filter_vods(vods, downloaded_vod_ids)

    for vod in vods_to_download:
        # Log downloaded VOD
        log_manager_.log_vod_download(vod)

        # Transcribe the video and log the transcription
        video_file_path = (
            f"downloads/{vod['id']}.mp4"  # Assume videos are saved in downloads folder
        )
        transcription = transcriber_.transcribe_video(video_file_path, vod["id"])

        if transcription:
            print(f"Transcription for VOD {vod['title']}", transcription)
        break

if __name__ == "__main__":
    main()
