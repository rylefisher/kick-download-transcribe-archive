import os
import subprocess
cwd = os.getcwd()

class HandbrakeConverter:
    def __init__(self, handbrake_cli_path=cwd + "/HandBrakeCLI.exe"):
        self.handbrake_cli_path = handbrake_cli_path

    def convert_video(self, input_path):
        if not os.path.exists(input_path):
            print(f"The file {input_path} does not exist.")
            return

        output_path = self._get_output_path(input_path)    
        # List of configurations to try in order: HEVC, QSV, Very Fast 720p
        configurations = [
            ("hevc", "veryfast"), # HEVC with very fast encoder
            ("qsv_h265", None),   # QSV if available (no extra preset)
            ("h264", "veryfast")  # Fallback: Very Fast 720p
        ]

        for (codec, preset) in configurations:
            command = [
                self.handbrake_cli_path,
                "-i", input_path,
                "-o", output_path,
                "--encoder", codec
            ]
            if preset:
                command.extend(["--preset", preset])

            try:
                subprocess.run(command, check=True)
                print(f"Conversion successful: {output_path}")  # Successful conversion
                self._delete_original(input_path)
                break
            except subprocess.CalledProcessError:
                print(f"Conversion failed with codec {codec}, trying next option.")

    def _get_output_path(self, input_path):
        base, _ = os.path.splitext(input_path)
        return f"{base}_converted.mp4"

    def _delete_original(self, input_path):
        try:
            os.remove(input_path)
            print(f"Original file deleted: {input_path}")
        except OSError as e:
            print(f"Error deleting original file: {e}")

if __name__ == "__main__":
    hbrake = HandbrakeConverter()
    vid_path = r"C:\Users\dower\Videos\Nuclear Content  New Warren Smith Video  Dani Attacked In The Streets In Japan .mp4"
    hbrake.convert_video(vid_path)
    hbrake