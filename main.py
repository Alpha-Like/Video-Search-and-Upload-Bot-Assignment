import os
import sys
import asyncio
import aiohttp
import argparse
from instaloader import Instaloader, Post
import shutil

FLIC_TOKEN = os.getenv('FLIC_TOKEN')

class Suppress:
    def __init__(self):
        self.stdout = None
    
    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, t, v, tb):
        sys.stdout = self.stdout

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Download Instagram reels and upload them to Socialverse.")
    parser.add_argument('url', help="Instagram reel URL")
    parser.add_argument('-t', '--title', help="Title for the post (optional)")
    parser.add_argument('-c', '--category_id', type=int, default=25, help="Category ID for the post (default: 25)")
    return parser.parse_args()

async def download_from_instagram(url: str) -> None:
    """
    Download an Instagram reel given its URL and save it to the 'videos' directory.
    """
    il = Instaloader()
    shortcode = url.split('reels/')[1].split('/')[0]
    post = Post.from_shortcode(il.context, shortcode)

    os.makedirs('videos', exist_ok=True)

    with Suppress():
        il.download_post(post, target='videos')

    for file in os.listdir('videos'):
        if not file.endswith('.mp4') and not file.endswith('.txt'):
            os.remove(os.path.join('videos', file))

async def generate_upload_url() -> dict:
    """
    Generate a pre-signed upload URL from the API.
    Returns the URL and hash as a dictionary.
    """
    endpoint = 'https://api.socialverseapp.com/posts/generate-upload-url'
    headers = {
        'Flic-Token': FLIC_TOKEN,
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to generate upload URL: {response.status}, {await response.text()}")

async def upload_video_to_url(upload_url: str, file_path: str) -> None:
    """
    Upload the video file to the server using the pre-signed URL.
    """
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            async with session.put(upload_url, data=file) as response:
                if response.status != 200:
                    raise Exception(f"Failed to upload video: {response.status}, {await response.text()}")

async def create_post(hash_value: str, title: str, category_id: int) -> None:
    """
    Create a post on the Socialverse platform using the video hash.
    """
    endpoint = 'https://api.socialverseapp.com/posts'
    headers = {
        'Flic-Token': FLIC_TOKEN,
        'Content-Type': 'application/json'
    }
    body = {
        "title": title,
        "hash": hash_value,
        "is_available_in_public_feed": False,
        "category_id": category_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, json=body) as response:
            if response.status != 200:
                raise Exception(f"Failed to create post: {response.status}, {await response.text()}")

async def process_reel(url: str, title: str = None, category_id: int = 25) -> None:
    """
    End-to-end process: download, upload, and create a post for an Instagram reel.
    """
    await download_from_instagram(url)

    video_files = [file for file in os.listdir('videos') if file.endswith('.mp4')]
    if not video_files:
        raise Exception("No video file found in 'videos' directory.")
    video_file_path = os.path.join('videos', video_files[0])

    upload_data = await generate_upload_url()
    upload_url = upload_data['url']
    hash_value = upload_data['hash']

    await upload_video_to_url(upload_url, video_file_path)

    if not title:
        title_file = [file for file in os.listdir('videos') if file.endswith('.txt')]
        if not title_file:
            title = 'A Video'
        else:
            title = open(os.path.join('videos', title_file[0]), 'r').read().strip()
    
    await create_post(hash_value, title, category_id)

    print(f"Process completed successfully for {url}: Video uploaded and post created.")

async def main():
    args = parse_arguments()

    try:
        await process_reel(args.url, args.title, args.category_id)
    except Exception as e:
        print(f"Error processing {args.url}: {e}")
    finally:
        if os.path.exists('videos'):
            shutil.rmtree('videos')

if __name__ == "__main__":
    asyncio.run(main())
