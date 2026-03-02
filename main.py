import requests
from PIL import Image
from io import BytesIO
import math
import ollama
import csv
from datetime import datetime
from pathlib import Path


def latlon_to_tile(lat, lon, zoom):
    """Convert lat/lon to OSM tile x/y numbers."""
    n = 2 ** zoom
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n)
    return x, y


def load_models_config():
    """Load model configuration from .models file."""
    config = {}
    with open(".models", "r") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                key, value = line.split("=", 1)
                config[key] = value.strip('"')
    return config


def get_osm_satellite_tile(lat, lon, zoom=15, save_path="./images/osm_tile.png"):
    """
    Fetches a satellite tile from ESRI's public World Imagery layer
    (free, no API key needed — check ESRI's ToS for your use case).
    """
    x, y = latlon_to_tile(lat, lon, zoom)
    # ESRI World Imagery (satellite)
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"

    headers = {"User-Agent": "Mozilla/5.0 (satellite-image-downloader)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    img = Image.open(BytesIO(response.content))
    img.save(save_path)
    print(f"Tile saved to: {save_path} — size: {img.size}")
    return img


def analyze_image_with_ollama(image_path, model_name):
    """Analyze an image using Ollama's vision model."""
    # Check if model exists locally
    try:
        models_list = ollama.list()
        model_exists = any(model.model.startswith(model_name) for model in models_list.models)

        if not model_exists:
            print(f"Model {model_name} not found locally. Pulling from Ollama...")
            ollama.pull(model_name)
            print(f"Successfully pulled {model_name}")
    except Exception as e:
        print(f"Error checking/pulling model: {e}")
        raise

    response = ollama.chat(
        model=model_name,
        messages=[{
            'role': 'user',
            'content': 'Describe this satellite image in detail. What can you see?',
            'images': [image_path]
        }]
    )
    return response['message']['content']


def save_to_csv(lat, lon, zoom, description, csv_path="./database/descriptions.csv"):
    """Append image metadata and description to CSV file."""
    file_exists = Path(csv_path).exists()

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header if file doesn't exist
        if not file_exists:
            writer.writerow(["timestamp", "latitude", "longitude", "zoom", "description"])

        timestamp = datetime.now().isoformat()
        writer.writerow([timestamp, lat, lon, zoom, description])

    print(f"Description saved to {csv_path}")


if __name__ == "__main__":
    # Load model configuration
    models = load_models_config()
    vision_model = models.get("VISION")

    # Coordinates for the Colosseum in Rome
    lat, lon, zoom = 41.8902, 12.4922, 17
    image_path = "./images/osm_tile.png"

    # Download satellite image
    print("Downloading satellite image...")
    get_osm_satellite_tile(lat, lon, zoom, save_path=image_path)

    # Analyze image with vision model
    print(f"Analyzing image with {vision_model}...")
    description = analyze_image_with_ollama(image_path, vision_model)
    print(f"\nDescription: {description}\n")

    # Save to CSV
    save_to_csv(lat, lon, zoom, description)

