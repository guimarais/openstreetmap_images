# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python utility for downloading satellite imagery tiles from OpenStreetMap-compatible tile servers. The project fetches satellite imagery tiles from ESRI's World Imagery layer based on latitude/longitude coordinates.

## Development Setup

The project uses `uv` as the package manager with Python 3.13+.

**Install dependencies:**
```bash
uv sync
```

**Run the script:**
```bash
uv run python main.py
```

## Project Structure

The codebase is currently a single-file utility (`main.py`) with two core functions:

- `latlon_to_tile(lat, lon, zoom)`: Converts geographic coordinates (latitude/longitude) to OSM tile coordinates (x, y) using the Web Mercator projection formula
- `get_osm_satellite_tile(lat, lon, zoom, save_path)`: Fetches a satellite image tile from ESRI's World Imagery server and saves it locally

## Key Technical Details

**Tile Server:**
- Uses ESRI World Imagery (publicly accessible, no API key required)
- URL format: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}`
- Check ESRI's Terms of Service for usage restrictions

**Coordinate System:**
- Standard OSM slippy map tile numbering scheme
- Web Mercator projection (EPSG:3857)
- Higher zoom levels = more detailed imagery (typical range: 0-19)

**Output:**
- Images saved to `./images/` directory by default
- Tile size: 256x256 pixels (standard OSM tile size)
