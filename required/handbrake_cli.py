import os
import subprocess
cwd = os.getcwd()  
class HandbrakeConverter:
    def __init__(self, working_dir=os.getcwd(), handbrake_cli_path="HandBrakeCLI"):  # fixed default directory and CLI path
        self.handbrake_cli_path = os.path.join(working_dir, handbrake_cli_path)  # use os.path.join for path

    def convert_video(self, input_path):
        # check if input file exists
        if not os.path.exists(input_path):
            print(f"The file {input_path} does not exist.")
            return

        output_path = self._get_output_path(input_path)

        # complete configuration based on provided CLI documentation
        configuration = [
            "--verbose=2",  # Increase verbosity level
            "-Z", "Very Fast 720p30",  # Set preset for fast 720p encoding
        ]

        command = [
            self.handbrake_cli_path,
            "-i", input_path,
            "-o", output_path
        ] + configuration

        try:
            subprocess.run(command, check=True)  # run conversion command
            print(f"Conversion successful: {output_path}")
            self._delete_original(input_path)  # delete original file
        except subprocess.CalledProcessError:
            print(f"Conversion failed for file: {input_path}")
        return output_path
    
    def _get_output_path(self, input_path):
        base, _ = os.path.splitext(input_path)
        return f"{base}_converted.mp4"  # output naming updated

    def _delete_original(self, input_path):
        try:
            os.remove(input_path)  # delete original file
            print(f"Original file deleted: {input_path}")
        except OSError as e:
            print(f"Error deleting original file: {e}")
            
if __name__ == "__main__":
    hbrake = HandbrakeConverter(cwd)
    vid_path = r"C:\Users\dower\Videos\Jstlk - Watch The Vod On Kick-03-05.10.31.464.mp4"
    hbrake.convert_video(vid_path)