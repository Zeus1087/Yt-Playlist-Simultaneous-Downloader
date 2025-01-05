import subprocess
import os

def download_playlist(playlist_url, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        command = [
            "yt-dlp",
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),  # Output template
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", # Best quality mp4
            playlist_url
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error downloading playlist:\n{stderr.decode()}")
        else:
            print(f"Playlist downloaded successfully to {output_path}")
            print(stdout.decode())

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
