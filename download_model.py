import os
import requests

def download_gpt4all_model(url, target_path):
    """
    Downloads the GPT4All model binary from the given URL and saves it to the target path.

    Args:
        url (str): URL to download the model from.
        target_path (str): Path to save the downloaded model.
    """
    try:
        print(f"Downloading GPT4All model from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(target_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Model downloaded successfully to {target_path}.")
    except Exception as e:
        print(f"Error downloading the model: {e}")

if __name__ == "__main__":
    # URL of the GPT4All model binary
    MODEL_URL = "https://gpt4all.io/installers/gpt4all-installer-linux.run"

    # Directory to save the model
    MODEL_DIR = "./model"
    MODEL_PATH = os.path.join(MODEL_DIR, "model.bin")

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    download_gpt4all_model(MODEL_URL, MODEL_PATH)
