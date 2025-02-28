import subprocess
import os


class HandbrakeConverter:
    def __init__(self, handbrake_cli_path="HandBrakeCLI.exe"):
        self.handbrake_cli_path = handbrake_cli_path

    def convert_video(self, input_path):
        if not os.path.exists(input_path):
            print(f"The file {input_path} does not exist.")
            return

        output_path = self._get_output_path(input_path)
        command = [
            self.handbrake_cli_path,
            "-i",
            input_path,
            "-o",
            output_path,
            "--preset",
            "Very Fast 1080p30",
        ]

        # Run the HandBrakeCLI command to convert the video
        try:
            subprocess.run(command, check=True)
            print(f"Conversion successful: {output_path}")
            self._delete_original(input_path)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during conversion: {e}")

    def _get_output_path(self, input_path):
        # Define the output path by changing the file extension to '.mp4'
        base, _ = os.path.splitext(input_path)
        return f"{base}_converted.mp4"

    def _delete_original(self, input_path):
        try:
            os.remove(input_path)
            print(f"Original file deleted: {input_path}")
        except OSError as e:
            print(f"Error deleting original file: {e}")


# Example usage:
# converter = HandbrakeConverter().convert_video('path/to/your/video.mkv')
# converter
