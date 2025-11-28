from langchain_core.tools import tool
import requests
import os

@tool
def download_file(url: str, filename: str) -> str:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        directory_name = "LLMFiles"
        os.makedirs(directory_name, exist_ok=True)
        path = os.path.join(directory_name, filename)
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return filename
    except Exception as e:
        return f"Error downloading file: {str(e)}"