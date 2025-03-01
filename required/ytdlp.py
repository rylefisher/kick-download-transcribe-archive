import os
import subprocess
from yt_dlp import YoutubeDL
from pathlib import Path


def download_video(url: str, base_download_path: str = ".") -> str:
    """Downloads a video using the specified format, tries 720p60 first, then best."""
    yt_dlp_path = "binaries\\yt-dlp.exe"
    def update_yt_dlp():
        """Update yt-dlp to the latest version."""
        try:
            # Run yt-dlp update command
            subprocess.run([yt_dlp_path, "-U"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Update error: {e}")

    def get_extension_from_filename(filename: str) -> str:
        """Extract file extension from the filename."""
        return os.path.splitext(filename)[1]

    update_yt_dlp()  # Ensure yt-dlp is updated

    outtmpl = os.path.join(base_download_path, "%(title)s.%(ext)s")
    cmd = [
        yt_dlp_path,  # Adjust for your yt-dlp executable
        "-f",
        "720p60/best",  # Format priority
        "-o",
        outtmpl,  # Output template
        url,
    ]
    try:
        # Use subprocess.run without capture_output for real-time printing
        completed_process = subprocess.run(cmd, check=True, text=True)
        output = completed_process.stdout
        print(output)

        lines = output.splitlines()
        downloaded_file = None
        for line in lines:
            if "Destination: " in line:
                downloaded_file = line.split(": ")[1]
                break

        if downloaded_file:
            extension = get_extension_from_filename(downloaded_file)
            filename_template = f"{os.path.splitext(downloaded_file)[0]}{extension}"
            return filename_template
        else:
            return ""
    except subprocess.CalledProcessError as e:
        print(f"Download error: {e.stderr}")
        return ""


def convert_to_wav(input_filepath: str, output_filepath: str) -> None:
    """Converts a file to WAV format using ffmpeg."""
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_filepath, output_filepath],
            check=True,  # use ffmpeg for conversion
        )
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}\n\nMAKE SURE FFMPEG IS IN SYS ENV VARS \n\n")

if __name__ == "__main__":
    test_url = "https://example.com/sample_video"
    download_path = "downloads"
    os.makedirs(download_path, exist_ok=True)  # ensure directory exists
    downloaded_file = download_video(test_url, download_path)
    if downloaded_file:
        wav_output = os.path.join(download_path, "output.wav")
        convert_to_wav(downloaded_file, wav_output)
