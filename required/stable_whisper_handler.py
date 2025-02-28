# transcriber.py
import os
import subprocess
from pathlib import Path
import stable_whisper

""""write a robust ammendment that breaks a long wav file (hours) into 60 second segments. the transcription has the best effect if its done 60 seconds at a time. take the audio and process one hour at a time. break the first hour into 60 second segments. then transcribe each segment. itll return json of the transcript. store the transcript to have a dict with the true timestamp (not the literal timestamp but the section of the original video as a key). then combine that first hour into json. then do the second hour the same, delete the 60 second wav segments at the end of each hour. combine all the hours together into one transcript. then return the json transcript. also, ensure if the video is less than an hour it works as well. """
import os
import subprocess
from pathlib import Path
import json
import stable_whisper

import os
import subprocess
from pathlib import Path
import json
import stable_whisper


class Transcriber:
    def __init__(self, log_manager=None, model_size="base"):
        self.model = stable_whisper.load_faster_whisper(model_size)
        if log_manager:
            self.log_manager = log_manager
        self.wav_path = ""

    def convert_to_wav(self, video_path):
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
        subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
        return self.wav_path

    def split_wav_to_segments(self, source_audio, segment_length=60):
        """Split audio into segments of a specified length."""
        base_name = os.path.splitext(source_audio)[0]
        segments = []
        
        try:
            # Get total duration of audio in seconds
            duration_output = subprocess.check_output([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", source_audio
            ])
            duration = float(duration_output.strip())  # Ensure duration is a float

            for start_time in range(0, int(duration), segment_length):
                segment_file = f"{base_name}_segment_{start_time}.wav"
                segments.append(segment_file)
                subprocess.run([
                    "ffmpeg", "-i", source_audio, "-ss", str(start_time),
                    "-t", str(segment_length), segment_file, "-y"
                ])
        except ValueError as e:
            print(f"Error parsing duration: {e}")
            raise

        return segments

    def transcribe_audio_segments(self, segments):
        """Transcribes each audio segment and returns their combined JSON."""
        combined_transcript = {}
        for segment in segments:
            result = self.model.transcribe(audio=segment, word_timestamps=True)
            segment_start = int(segment.split('_')[-1].replace('.wav', ''))  # Ensure this is int-compatible
            combined_transcript[segment_start] = result.to_dict()

            # Remove the segment after transcription
            os.remove(segment)
        return combined_transcript

    def transcribe_video(self, video_path):
        try:
            audio_path = self.convert_to_wav(video_path)
            segments = self.split_wav_to_segments(audio_path, segment_length=60)

            result_json = {}
            segment_count = len(segments)
            hours = (segment_count * 60) // 3600 + 1  # total hours in the video

            for hour in range(hours):
                hour_segments = segments[hour * 60 : (hour + 1) * 60]
                hour_transcript = self.transcribe_audio_segments(hour_segments)
                
                if hour_transcript:
                    result_json.update(hour_transcript)

            combined_json_path = audio_path.replace('.wav', '_transcript.json')
            with open(combined_json_path, 'w') as json_file:
                json.dump(result_json, json_file)

            return result_json

        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return None
