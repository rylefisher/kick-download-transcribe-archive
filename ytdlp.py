import os
import subprocess
from yt_dlp import YoutubeDL


def download_video(url: str, download_path: str = ".") -> str:
    """Downloads a video and returns the file path."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
        "n_threads": 4,  # maximize threads
        "progress_hooks": [  # status updates
            lambda d: print(f"Status: {d['status']}: {d.get('filename', 'Unknown')}")
        ],
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(result)  # get output filename
        return downloaded_file
    except Exception as e:
        print(f"Download error: {e}")
        return ""


def convert_to_wav(input_filepath: str, output_filepath: str) -> None:
    """Converts a file to WAV format using ffmpeg."""
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_filepath, output_filepath],
            check=True,  # use ffmpeg for conversion
        )
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")


# Example usage
if __name__ == "__main__":
    test_url = "https://example.com/sample_video"
    download_path = "downloads"
    os.makedirs(download_path, exist_ok=True)  # ensure directory exists
    downloaded_file = download_video(test_url, download_path)
    if downloaded_file:
        wav_output = os.path.join(download_path, "output.wav")
        convert_to_wav(downloaded_file, wav_output)
