import requests
from PIL import Image
from io import BytesIO
import math


def latlon_to_tile(lat, lon, zoom):
    """Convert lat/lon to OSM tile x/y numbers."""
    n = 2 ** zoom
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n)
    return x, y


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


if __name__ == "__main__":
    # Gets the coloseum in Rome
    get_osm_satellite_tile(41.8902, 12.4922, zoom=17)

