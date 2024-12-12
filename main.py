import os
import sys
import asyncio
import aiohttp
from instaloader import Instaloader, Post
import shutil

FLIC_TOKEN = os.getenv('FLIC_TOKEN')

async def download_from_instagram(url: str) -> None:
    """
    Download an Instagram reel given its URL and save it to the 'videos' directory.
    """
    il = Instaloader()
    shortcode = url.split('reels/')[1].split('/')[0]
    post = Post.from_shortcode(il.context, shortcode)

    os.makedirs('videos', exist_ok=True)

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

async def create_post(hash_value: str, title: str, category_id: int = 69) -> None:
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

async def process_reel(url: str) -> None:
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

    title_file = [file for file in os.listdir('videos') if file.endswith('.txt')]
    if not title_file:
        raise Exception("No title file found in 'videos' directory.")
    title = open(os.path.join('videos', title_file[0]), 'r').read()
    
    await create_post(hash_value, title)

    print(f"Process completed successfully for {url}: Video uploaded and post created.")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <url1> <url2> ...")
        sys.exit(1)

    urls = sys.argv[1:]
    for url in urls:
        try:
            await process_reel(url)
        except Exception as e:
            print(f"Error processing {url}: {e}")
        finally:
            if os.path.exists('videos'):
                shutil.rmtree('videos')

if __name__ == "__main__":
    asyncio.run(main())
