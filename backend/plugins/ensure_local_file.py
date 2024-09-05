import os
import requests
import tempfile
from urllib.parse import urlparse


def EnsureLocalFile(source):
    """
    Ensures that the source is available as a local file. If the source is a URL,
    the content is downloaded and stored in a temporary file. If it's a local file,
    it returns the original path.

    :param source: The path to the local file or a URL.
    :return: The path to a local file.
    """
    # Check if source is a URL
    parsed_url = urlparse(source)
    if parsed_url.scheme in ('http', 'https'):
        # It's a URL, download the file content
        response = requests.get(source)
        if response.status_code == 200:
            # Create a temporary file
            _, ext = os.path.splitext(parsed_url.path)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            with open(temp_file.name, 'wb') as f:
                f.write(response.content)
            return temp_file.name
        else:
            raise ValueError("Failed to download the file from the URL")
    elif os.path.exists(source):
        # It's a local file, return the path directly
        return source
    else:
        raise ValueError("The source is neither a valid URL nor an existing local file")