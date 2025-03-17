# main.py
try:
    import required.stable_whisper_handler as stable_whisper_handler  # Import Transcriber
except Exception as e:
    print('accessing module directly, bypassing required folder import')
import os

"""used for testing and or skipping the download process"""

def transcribe_video(video_path, v_id, log_folder, rumble_url):
    wav_output = video_path.split('.mp4')[0] + "_output.wav"
    swhisper_ = stable_whisper_handler.Transcriber()
    transcription = swhisper_.transcribe_video(video_path)
    swhisper_.write_html(transcription, v_id, log_folder, rumble_url)
    if transcription:
        print(f"Transcription for VOD {video_path}", transcription)
    return transcription 

if __name__ == "__main__":
    import stable_whisper_handler as stable_whisper_handler  # Import Transcriber
    vid_path = r"C:\Users\dower\Videos\Jstlk - Watch The Vod On Kick-03-05.10.31.464(1).mp4"

    # VID_PATH = file_management.clean_path(VID_PATH)
    transcribe_video(vid_path, "03-05.10.31.464(1)")
