# 🏏 IBS TV Special Sports

This repository contains an automated system to fetch, clean, and generate updated M3U playlists for live sports events from Crichd sources. It is designed to provide high-quality streams along with dynamic promotions and neat organization for end-users.

## Features
- **Auto Update:** Automatically updates the playlist every 30 minutes.
- **Random Promotions:** Randomly appends dynamic promotion videos at the beginning of each category.
- **Smart Formatting:** Cleans raw Crichd names and groups channels properly.
- **Dedicated Branch:** Managed on the `M3u8` branch to keep the main repository clean.

## Requirements
- Python 3.x
- `requests` and `pytz` libraries

## Usage
The system processes the following sources:
- Go Live Events
- Crichd Live Events
- Crichdat Live Events

Generated output is saved directly to: `IBS TV special.m3u`

## Workflow (Automation)
The `.github/workflows/crichd.yml` uses GitHub Actions to run `crichd.py` on a schedule, ensuring users always get the freshest links.
