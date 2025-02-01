#testing phase

import yt_dlp
import tweepy
import json
from datetime import datetime
from pathlib import Path
import time
from yt_dlp import YoutubeDL
import os
import re
import subprocess

# Your API Keys
api_key = "6Ar5ncMwhHdnQs1cl8AchNeXe"
api_secret = "dkNDJkHRX4GIp5bUofjTBTx7Te6eQvDpcigpQb2ScZf7tEEvdA"

# Create both v1.1 and v2 clients for media upload support
auth1 = tweepy.OAuth1UserHandler(
    "6Ar5ncMwhHdnQs1cl8AchNeXe",
    "dkNDJkHRX4GIp5bUofjTBTx7Te6eQvDpcigpQb2ScZf7tEEvdA",
    "1724776081180520448-2vok1HeYy8edq9wgs7b7BrTwuu6qGq",
    "y0kLRyGY7oAmekZY1Y2xRomTL9WkP5Uii839MQESdiKEW"
)
api1 = tweepy.API(auth1)

client1 = tweepy.Client(
    consumer_key="6Ar5ncMwhHdnQs1cl8AchNeXe",
    consumer_secret="dkNDJkHRX4GIp5bUofjTBTx7Te6eQvDpcigpQb2ScZf7tEEvdA",
    access_token="1724776081180520448-2vok1HeYy8edq9wgs7b7BrTwuu6qGq",
    access_token_secret="y0kLRyGY7oAmekZY1Y2xRomTL9WkP5Uii839MQESdiKEW"
)

# Create both v1.1 and v2 clients for media upload support
auth2 = tweepy.OAuth1UserHandler(
    "XfLuXMo7XtPHCXvOTQgGRjKkC",
    "Biq8PFrqPEeEsAw2jxuAE24hYVsEVYNtNde3RpWjHmFX5hkoRw",
    "1796410560403341312-HTj94WDsW4GoDQdti6p0Rbkb2SzsOg",
    "t40d9xZhnNwyBteYvpz7ibLdgpHUXplmR58CDWbrkADA2"
)
api2 = tweepy.API(auth2)

client2 = tweepy.Client(
    consumer_key="XfLuXMo7XtPHCXvOTQgGRjKkC",
    consumer_secret="Biq8PFrqPEeEsAw2jxuAE24hYVsEVYNtNde3RpWjHmFX5hkoRw",
    access_token="1796410560403341312-HTj94WDsW4GoDQdti6p0Rbkb2SzsOg",
    access_token_secret="t40d9xZhnNwyBteYvpz7ibLdgpHUXplmR58CDWbrkADA2"
)

# Create both v1.1 and v2 clients for media upload support
auth3 = tweepy.OAuth1UserHandler(
    "lzxvOMvzkwCsrc8t9xzevrJ2G",
    "O9LcyPFpH2f7a4CsycGMjlykuC0OfVvp0trNe7GXOfVCwPB0Pm",
    "1874741482319736832-GCcGrZdiGQqYcy27TkguR4YVV6rtYo",
    "Q8n9v8mQw0HmicAGkVnzDGbZy8zU9nnaJRIKWXdYsJ4fH"
)
api3 = tweepy.API(auth3)

client3 = tweepy.Client(
    consumer_key="lzxvOMvzkwCsrc8t9xzevrJ2G",
    consumer_secret="O9LcyPFpH2f7a4CsycGMjlykuC0OfVvp0trNe7GXOfVCwPB0Pm",
    access_token="1874741482319736832-GCcGrZdiGQqYcy27TkguR4YVV6rtYo",
    access_token_secret="Q8n9v8mQw0HmicAGkVnzDGbZy8zU9nnaJRIKWXdYsJ4fH"
)

# URL of the YouTube Short
video_url = "https://www.youtube.com/shorts/pWAqeig94sU"

# Download the video
#download_youtube_short(video_url)

def clean_filename(title, max_length=50):
    """Clean the title to make it a valid filename"""
    clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
    clean_title = ' '.join(clean_title.split())
    if len(clean_title) > max_length:
        clean_title = clean_title[:max_length].rsplit(' ', 1)[0]
    return clean_title.strip()

def convert_video_to_h264(input_file, output_file):
    """Convert video to H.264 format"""
    try:
        # FFmpeg command to convert video to H.264
        command = [
            "ffmpeg",
            "-i", input_file,  # Input file
            "-c:v", "libx264",  # Video codec: H.264
            "-c:a", "aac",      # Audio codec: AAC
            "-strict", "experimental",  # Allow experimental features
            "-b:v", "2M",       # Video bitrate
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=30",  # Scaling and FPS
            output_file
        ]

        # Run the command
        subprocess.run(command, check=True)
        print(f"Conversion successful! Saved as: {output_file}")
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e)
    except Exception as ex:
        print("An unexpected error occurred:", ex)

def read_urls_file(filename='urls2.txt'):
    """Read URLs from the specified file"""
    try:
        with open(filename, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []

def process_next_url(urls,urlpath,api,client):
    """Process the next URL in the list and rotate it to the end"""
    if not urls:
        print("No URLs available in the file")
        return

    # Get the first URL and rotate the list
    url = urls[0]
    urls = urls[1:] + [urls[0]]

    # Write the rotated URLs back to the file
    with open(urlpath, 'w') as file:
        file.write('\n'.join(urls))

    # Process the URL
    print(f"Processing URL: {url}")
    video_info = download_and_get_info(url)

    if video_info:
        # Convert the downloaded video
        converted_filename = f"{Path(video_info['filename']).stem}_converted.mp4"
        convert_video_to_h264(video_info['filename'], converted_filename)

        # Update video info with converted filename
        video_info['filename'] = converted_filename
        post_and_cleanup(video_info,api,client)
    else:
        print("Failed to download video")

def download_and_get_info(url):
    """Download video and return video information"""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Prefer MP4 format
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return {
                'filename': filename,
                'title': clean_filename(info.get('title', 'YouTube Short')),
                'url': url
            }
    except Exception as e:
        print(f"An error occurred during download: {str(e)}")
        return None

def download_and_get_info(url):
    """Download video and return video information"""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Prefer MP4 format
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'cookiefile': 'cookies.txt',  # Add this line to use the cookies file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return {
                'filename': filename,
                'title': clean_filename(info.get('title', 'YouTube Short')),
                'url': url
            }
    except Exception as e:
        print(f"An error occurred during download: {str(e)}")
        return None



def post_and_cleanup(video_info,api,client):
    """Post a video to Twitter and delete it afterward"""
    if not video_info:
        print("No video information provided")
        return

    try:
        print("Uploading media to Twitter...")
        # Upload media
        media = api.media_upload(video_info['filename'])

        # Create tweet
        tweet_text = "Follow for more !!" #\n\nOriginal: {video_info['url']}"
        print("Posting tweet...")
        response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])

        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")

        # Get the original filename (before conversion)
        original_filename = video_info['filename'].replace('_converted.mp4', '.mp4')

        # Delete the downloaded video
        if os.path.exists(video_info['filename']):
            os.remove(video_info['filename'])
            print(f"Deleted video file: {video_info['filename']}")

        if os.path.exists(original_filename):
            os.remove(original_filename)
            print(f"Deleted original video file: {original_filename}")

    except Exception as e:
        print(f"Error posting tweet: {e}")
        # Cleanup even if posting fails
        original_filename = video_info['filename'].replace('_converted.mp4', '.mp4')
        for file in [video_info['filename'], original_filename]:
            if os.path.exists(file):
                os.remove(file)
                print(f"Cleaned up file after error: {file}")


def main():
    """print("Starting YouTube Short to Twitter trial...")
    video_url = "https://www.youtube.com/shorts/E0KYVZd-P34"  # Fix: Define video_url
    video_info = download_and_get_info(video_url)

    if video_info:
        # Convert the downloaded video
        converted_filename = f"{Path(video_info['filename']).stem}_converted.mp4"
        convert_video_to_h264(video_info['filename'], converted_filename)

        # Update video info with converted filename
        video_info['filename'] = converted_filename
        post_and_cleanup(video_info)
    else:
        print("Failed to download video")"""

    """while True:
        print("\nStarting YouTube Short to Twitter process...")
        try:
            urls = read_urls_file()
            if urls:
                process_next_url(urls)
            else:
                print("No URLs found in urls.txt")
        except Exception as e:
            print(f"An error occurred in main loop: {e}")

        print(f"Waiting for 3 hours before next execution...")
        time.sleep(500)  # Sleep for 3 hours"""
    '''while True:
        print("\nStarting YouTube Short to Twitter process...")
        try:
            urls = read_urls_file('urls2.txt')
            if urls:
                process_next_url(urls,'urls2.txt',api1,client1)
            else:
                print("No URLs found in urls.txt")
        except Exception as e:
            print(f"An error occurred in main loop: {e}")
        try:
            urls = read_urls_file('urls2.txt')
            if urls:
                process_next_url(urls,'urls2.txt',api2,client2)
            else:
                print("No URLs found in urls.txt")
        except Exception as e:
            print(f"An error occurred in main loop: {e}")
        try:
            urls = read_urls_file('urls2.txt')
            if urls:
                process_next_url(urls,'urls2.txt',api3,client3)
            else:
                print("No URLs found in urls.txt")
        except Exception as e:
            print(f"An error occurred in main loop: {e}")'''
    print("Hello")

        print(f"Waiting for 3 hours before next execution...")
        time.sleep(3*60*60)  # Sleep for 3 hours

if __name__ == "__main__":
    main()
