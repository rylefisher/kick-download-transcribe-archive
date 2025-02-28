# main.py
import firefox_linkgrabber
import log_manager
import transcriber  # Import Transcriber
import ytdlp
import os 

FIREFOX = r"D:\Documents\FirefoxPortable\App\Firefox64\firefox.exe"

def main():
    # Initialize LogManager
    log_manager_ = log_manager.LogManager(project_name="VODDownloader")
    # Initialize Transcriber
    transcriber_ = transcriber.Transcriber(log_manager=log_manager_)
    vods = firefox_linkgrabber.main(FIREFOX)

    # bypass for testing purposes
    downloaded_vods = log_manager_.get_downloaded_vods()

    # Filter VODs - bypass for testing purposes
    # vods_to_download = log_manager_.filter_vods(vods, downloaded_vod_ids)

    for vod in vods:
        # Log downloaded VOD
        idn = vod.split('/')[-1]
        download_path = str(log_manager_.base_dir) + f"/{idn}"
        log_manager_.log_vod_download(vod)
        downloaded_file = ytdlp.download_video(vod, download_path)
        if downloaded_file:
            wav_output = os.path.join(download_path, "output.wav")
            ytdlp.convert_to_wav(downloaded_file, wav_output)

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
