  README - Instagram Reel Uploader

Instagram Reel Uploader
=======================

This Python script automates the process of downloading Instagram reels, uploading them to a server, and creating a post on the Socialverse platform.

Features
--------

*   Download reels from Instagram using their URL.
*   Generate a pre-signed upload URL from Socialverse API.
*   Upload the downloaded reel to the server.
*   Create a Socialverse post with a title and category ID.

Prerequisites
-------------

*   Python 3.7 or higher
*   Pip-installed packages:
    *   `aiohttp`
    *   `instaloader`
*   Set the environment variable `FLIC_TOKEN` with a valid token for API access.

Installation
------------

    pip install aiohttp instaloader
    

Usage
-----

Run the script from the command line with the following syntax:

    python3 main.py  \[-t \] \[-c <category\_id>\]
    </pre>

    <h3>Arguments:</h3>
    <ul>
        <li><code>url</code>: The URL of the Instagram reel to process (required).</li>
        <li><code>-t</code>, <code>--title</code>: Optional title for the post. If not provided, the script reads the title from a <code>.txt</code> file downloaded with the reel.</li>
        <li><code>-c</code>, <code>--category\_id</code>: Optional category ID for the post. Default is <code>25</code>.</li>
    </ul>

    <h2>Example</h2>
    <pre>
    python3 main.py https://www.instagram.com/reels/example-reel/ -t "My Reel" -c 69
    </pre>
    <p>If the title is not specified:</p>
    <pre>
    python3 main.py https://www.instagram.com/reels/example-reel/
    </pre>

    <h2>Workflow</h2>
    <ol>
        <li>Downloads the Instagram reel and associated metadata using <code>Instaloader</code>.</li>
        <li>Generates a pre-signed upload URL from the Socialverse API.</li>
        <li>Uploads the reel video to the server using the generated URL.</li>
        <li>Creates a Socialverse post with the provided or extracted title and category ID.</li>
    </ol>

    <h2>Error Handling</h2>
    <p>The script includes error handling for the following scenarios:</p>
    <ul>
        <li>Invalid or inaccessible Instagram URL.</li>
        <li>Missing video or title file after download.</li>
        <li>Failed API calls for generating upload URLs or creating posts.</li>
    </ul>

    <h2>Cleaning Up</h2>
    <p>After processing, the script cleans up by deleting the <code>videos</code> directory.</p>

    <h2>License</h2>
    <p>MIT License</p>
</body>
</html>
</x-turndown>
