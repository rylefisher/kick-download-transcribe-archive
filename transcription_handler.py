# main.py
import firefox_linkgrabber
import log_manager
import stable_whisper_handler  # Import Transcriber
import ytdlp
import os

"""used for testing and or skipping the download process"""
VID_PATH = "C:\Users\dower\Documents\VODDownloader\0fa974ab-cdc0-4e6c-a6a2-3dadc91ea6cb\NUCLEAR CONTENT☢️NEW WARREN SMITH VIDEO 😱DANI ATTACKED IN THE STREETS IN JAPAN👊.mp4"

def main(vid=None):
    if vid == None:
        vid = VID_PATH
    
    wav_output = os.path.join(vid.split('.mp4')[0], "output.wav")
    ytdlp.convert_to_wav(vid, wav_output)
 
    transcription = stable_whisper_handler.Transcriber.transcribe_video(vid)

    if transcription:
        print(f"Transcription for VOD {vid}", transcription)
    return transcription 

if __name__ == "__main__":
    main()
