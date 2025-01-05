import subprocess
import os
import re

def download_playlist(playlist_url, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        command = [
            "yt-dlp",
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--progress", #this is important for progress bar
            playlist_url
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # text=true is important

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                match = re.search(r"\[download\]\s*([\d.]+)% of", output) #regex to find percentage
                if match:
                    percentage = match.group(1)
                    print(f"Download Progress: {percentage}%", end="\r") #\r to overwrite the line
                else:
                    print(output.strip()) #print other yt-dlp output

        if process.returncode != 0:
            _, stderr = process.communicate()
            print(f"Error downloading playlist:\n{stderr}")
        else:
            print("\nPlaylist downloaded successfully!")

    except FileNotFoundError:
        print("yt-dlp is not installed. Please install it using: pip install yt-dlp")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    output_path = input("Enter the output directory (or press Enter for current directory): ")
    if not output_path:
        output_path = "."

    download_playlist(playlist_url, output_path)
