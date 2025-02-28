# main.py
import firefox_linkgrabber
import log_manager
import stable_whisper_handler  # Import Transcriber
import ytdlp
import os
import file_management



"""used for testing and or skipping the download process"""
VID_PATH = r"C:\Users\dower\Documents\VODDownloader\0fa974ab-cdc0-4e6c-a6a2-3dadc91ea6cb\NUCLEAR_CONTENT__NEW_WARREN_SMITH_VIDEO__DANI_ATTACKED_IN_THE_STREETS_IN_JAPAN_.mp4"
VID_PATH = file_management.clean_path(VID_PATH)

def main(vid=None):
    if vid == None:
        vid = VID_PATH
    
    wav_output = vid.split('.mp4')[0] + "_output.wav"
 
    trans_obj = stable_whisper_handler.Transcriber()
    transcription = trans_obj.transcribe_video(vid)

    if transcription:
        print(f"Transcription for VOD {vid}", transcription)
    return transcription 

if __name__ == "__main__":
    main()
