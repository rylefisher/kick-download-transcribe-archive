# main.py
import required.firefox_linkgrabber as firefox_linkgrabber
import required.log_manager as log_manager
import required.stable_whisper_handler as stable_whisper_handler  # Import Transcriber
import required.ytdlp as ytdlp
import os
import required.file_management as file_management

"""used for testing and or skipping the download process"""

def main(vid):
    wav_output = vid.split('.mp4')[0] + "_output.wav"
    trans_obj = stable_whisper_handler.Transcriber()
    transcription = trans_obj.transcribe_video(vid)

    if transcription:
        print(f"Transcription for VOD {vid}", transcription)
    return transcription 

if __name__ == "__main__":
    vid_path = r"C:\Users\dower\Videos\Nuclear Content  New Warren Smith Video  Dani Attacked In The Streets In Japan .mp4"
    # VID_PATH = file_management.clean_path(VID_PATH)
    main(vid_path)
