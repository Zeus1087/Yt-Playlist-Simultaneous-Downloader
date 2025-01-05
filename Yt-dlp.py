import subprocess
import os
import re
import time

def download_playlist(playlist_url, output_path, max_concurrent_downloads=4): #parameter for concurrent downloads
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        command = [
            "yt-dlp",
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--progress",
            "--newline",
            "-N", str(max_concurrent_downloads), # Concurrent downloads
            "--fragment-retries", "infinite", # Retry fragments
            playlist_url
        ]

        #Using aria2c if available
        if subprocess.run(["which", "aria2c"], capture_output=True).returncode == 0:
            command.extend(["--external-downloader", "aria2c"])
            print("Using aria2c for potentially faster downloads.")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        total_files = None
        downloaded_files = 0

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if total_files is None:
                    match_total = re.search(r"Downloading (\d+) videos", output)
                    if match_total:
                        total_files = int(match_total.group(1))
                        print("Total videos to download:", total_files)
                match = re.search(r"\[download\]\s*([\d.]+)% of", output)
                if match:
                  pass
                elif "Finished downloading" in output:
                    downloaded_files += 1
                    if total_files:
                        percentage = (downloaded_files / total_files) * 100
                        print(f"[{'='*int(percentage//5)}{' '*(20-int(percentage//5))}] {percentage:.1f}%", end="\r")
                    else:
                        print("Downloading...", end="\r")
        if total_files is None:
            print("Could not get total files")
        elif downloaded_files == total_files:
            print(f"[{'='*20}] 100.0%")
            print("Playlist downloaded successfully!")
        elif process.returncode != 0:
            _, stderr = process.communicate()
            print(f"Error downloading playlist:\n{stderr}")
        else:
            print("Download Interrupted or incomplete.")

    except FileNotFoundError:
        print("yt-dlp is not installed. Please install it using: pip install yt-dlp")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    output_path = input("Enter the output directory (or press Enter for current directory): ")
    if not output_path:
        output_path = "."
    max_concurrent = int(input("Enter the maximum number of concurrent downloads (default is 4):") or 4)
    download_playlist(playlist_url, output_path, max_concurrent)
