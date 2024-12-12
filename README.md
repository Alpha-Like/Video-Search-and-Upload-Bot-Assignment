  Instagram Video Downloader and Uploader

Instagram Video Downloader and Uploader
=======================================

This Python script automates the process of downloading Instagram videos, uploading them to a specified server, and creating a post using an API. It simplifies the workflow for handling multiple Instagram video URLs at once.

* * *

Features
--------

*   **Download Instagram Videos:** Extract and download videos using their public URL.
*   **Upload to Server:** Upload the downloaded video files to a server via a pre-signed URL.
*   **Create Posts:** Automate post creation on the server with customizable titles and categories.
*   **Batch Processing:** Accept multiple Instagram video URLs as command-line arguments.
*   **Error Handling:** Resilient to individual failures; continues processing other URLs.

* * *

Requirements
------------

### Python Libraries

Install the required libraries using pip:

    pip install aiohttp instaloader

### Environment Variables

Set the `FLIC_TOKEN` environment variable with your API token for authentication:

    export FLIC_TOKEN="your_flic_token_here"

* * *

Usage
-----

### Running the Script

1.  Save the script to a file, e.g., `main.py`.
2.  Pass Instagram video URLs as arguments:

    python3 main.py <url1> <url2> ...

### Example

    python3 main.py https://www.instagram.com/reels/C_xnrVHyN7Y/ https://www.instagram.com/reels/C_yabVHzZ8K/
