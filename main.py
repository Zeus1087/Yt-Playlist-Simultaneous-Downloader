import pytube
import asyncio
import aiohttp
import os

async def download_video(session, url, output_path):
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.get_highest_resolution()
        if stream:
            print(f"Downloading: {yt.title}")
            async with session.get(stream.url) as response:
                if response.status == 200:
                    file_size = int(response.headers.get("Content-Length", 0))
                    downloaded = 0
                    with open(os.path.join(output_path, f"{yt.title}.mp4"), "wb") as f:
                        async for chunk in response.content.iter_chunked(1024):  # Download in chunks
                            f.write(chunk)
                            downloaded += len(chunk)
                            print(f"{yt.title}: {downloaded/file_size*100:.2f}%", end='\r') #Progress bar
                    print(f"\nFinished: {yt.title}")
                else:
                    print(f"Error downloading {url}: Status code {response.status}")
        else:
            print(f"No suitable stream found for {url}")
    except pytube.exceptions.RegexMatchError:
        print(f"Invalid YouTube URL: {url}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def download_playlist(playlist_url, output_path):
    try:
        playlist = pytube.Playlist(playlist_url)
        video_urls = playlist.video_urls
        print(f"Downloading {len(video_urls)} videos from playlist: {playlist.title}")

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        async with aiohttp.ClientSession() as session:
            tasks = [download_video(session, url, output_path) for url in video_urls]
            await asyncio.gather(*tasks)

        print("Playlist download complete!")
    except pytube.exceptions.RegexMatchError:
        print("Invalid playlist URL.")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    output_path = input("Enter the output directory (or press Enter for current directory): ")
    if not output_path:
        output_path = "." # Current Directory

    asyncio.run(download_playlist(playlist_url, output_path))
