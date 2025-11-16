#!/usr/bin/env python3
import argparse
from pathlib import Path

from rice_backend import apply_style, generate_palette, apply_wallpaper

def main():
    parser = argparse.ArgumentParser(description="Rice Manager CLI")
    parser.add_argument("-w", "--wallpaper", help="Chemin vers un wallpaper à appliquer")
    parser.add_argument("-s", "--style", nargs=2, metavar=("APP", "STYLE"), help="Appliquer un style à une app")
    parser.add_argument("-r", "--reload", action='store_true')
    args = parser.parse_args()

    if args.wallpaper:
        apply_wallpaper(Path(args.wallpaper))

    if args.reload:
        generate_thumbnails()

    if args.style:
        app, style = args.style
        apply_style(app, style)

if __name__ == "__main__":
    main()
