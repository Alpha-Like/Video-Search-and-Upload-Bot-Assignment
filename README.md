  Instagram Reel Downloader and Socialverse Uploader

Instagram Reel Downloader and Socialverse Uploader
==================================================

This script allows you to download Instagram Reels and upload them to the Socialverse platform.

Requirements
------------

*   Python 3.x
*   aiohttp library (install with \`pip install aiohttp\`)
*   instaloader library (install with \`pip install instaloader\`)
*   A Socialverse account with Flic Token

Usage
-----

1. **Set environment variable:**

Set an environment variable named `FLIC_TOKEN` with your Socialverse Flic Token.

2. **Run the script:**

bash 
```
python3 main.py url -t "Your Title" -c 25
```

*   **url**: Replace this with the URL of the Instagram Reel you want to download.
*   **\-t "Your Title" (optional)**: Specify a title for the Socialverse post.
*   **\-c 25 (optional)**: Set the category ID for the Socialverse post (default is 25).

Functionality
-------------

*   Downloads the Instagram Reel video using Instaloader.
*   Generates a pre-signed upload URL from Socialverse API.
*   Uploads the video to Socialverse using the pre-signed URL.
*   Creates a new post on Socialverse with the uploaded video.
*   Optionally reads title from a ".txt" file in the downloaded video directory.
*   Cleans up the downloaded video files after successful upload.
