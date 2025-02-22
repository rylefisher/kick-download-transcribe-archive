# transcriber.py
import os
import subprocess
from pathlib import Path
import stable_whisper


class Transcriber:
    def __init__(self, log_manager, model_size="medium"):
        # Initialize the transcriber with a model and log manager
        self.model = stable_whisper.load_faster_whisper(model_size)
        self.log_manager = log_manager
        self.wav_path = ""
        
    def convert_to_wav(self, video_path):
        # Convert video to wav using ffmpeg
        self.wav_path = str(Path(video_path).with_suffix(".wav"))
        command = [
            "ffmpeg",
            "-i",
            video_path,
            "-ac",
            "1",
            "-ar",
            "16000",
            self.wav_path,
            "-y",
        ]

        subprocess.run(
            command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True
        )  # Ensure conversion is error-free
        return self.wav_path

    def transcribe_video(self, video_path, vod_id):
        try:
            # Convert video to a compatible audio format
            audio_path = self.convert_to_wav(video_path)

            # Transcribe the audio using the Faster Whisper model
            result = self.model.transcribe(audio=audio_path, word_timestamps=True)

            # Save the transcription result to a file in JSON format
            json_path = self.log_manager.base_dir / f"{vod_id}_transcription.json"
            result.save_as_json(str(json_path))

            # Save transcription data to logs
            transcription_data = (
                result.to_dict()
            )  # Assuming to_dict() provides a proper dictionary
            self.log_manager.log_transcription(vod_id, transcription_data)

            return transcription_data
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return None
