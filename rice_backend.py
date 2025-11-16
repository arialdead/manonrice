#!/usr/bin/env python3
import os, subprocess, json, shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# ----------------------- CONFIG -----------------------
RICE_DIR = Path.home() / "gamesoft" / "ariceal" 
APPS_DIR = RICE_DIR / "apps"
WALLPAPERS_DIR = RICE_DIR / "wallpapers"
THUMBNAILS_DIR = RICE_DIR / "wallpapers_thumbnails"
PRESETS_DIR = RICE_DIR / "presets"
SWWW_BIN = shutil.which("swww") or "swww"
PYWAL_BIN = shutil.which("wal") or None

# ----------------------- FIN CONFIG -------------------

env = Environment(loader=FileSystemLoader(str(APPS_DIR)))

# ----------------------- Helpers ---------------------
def run_cmd(cmd_list):
    try:
        print("Running:", cmd_list)  # debug
        subprocess.run(cmd_list, check=False)
    except Exception as e:
        print("Error:", e)

def generate_palette(img_path):
    """Génère une palette de couleurs depuis le wallpaper avec pywal."""
    if PYWAL_BIN and img_path and Path(img_path).exists():
        run_cmd([PYWAL_BIN, "-i", str(img_path), "-n", "-q"])
        cache = Path.home() / ".cache/wal/colors.json"
        if cache.exists():
            data = json.loads(cache.read_text())
            special = data.get("special", {})
            background = special.get("background")
            foreground = special.get("foreground")
            colors_dict = data.get("colors", {})
            print("Colors_dict : %s" % colors_dict)
            palette = {**colors_dict, "background": background, "foreground": foreground}
            return palette
    return {"primary":"#222","accent1":"#f55","accent2":"#5f5","accent3":"#50fa7b","background":"#000","text":"#fff"}

def load_palette():
    cache = Path.home() / ".cache/wal/colors.json"
    if cache.exists():
        data = json.loads(cache.read_text())
        special = data.get("special", {})
        background = special.get("background")
        foreground = special.get("foreground")
        colors_dict = data.get("colors", {})
        palette = {**colors_dict, "background": background, "foreground": foreground}
        return palette

def style_meta(style, app_name):
    meta_file = APPS_DIR / app_name / "styles" / style / "meta.json"
    return json.loads(meta_file.read_text())

def apply_style(app_name, style):
    print(app_name)
    meta = style_meta(style, app_name)
    style_path = APPS_DIR / app_name / "styles" / style / meta["src"]
    target = meta["target"]
    typ = meta["type"]

    palette = load_palette()

    temp_file = RICE_DIR / "current_setup.json"
    temp_json = json.loads(temp_file.read_text())
    temp_json[str(app_name)] = str(style)
    temp_file.write_text(json.dumps(temp_json, indent=4))

    if typ == "fixed":
        shutil.copy2(style_path, Path(target).expanduser())
    else:
        tmpl = env.get_template(f"{app_name}/styles/{style}/{meta['src']}")
        rendered = tmpl.render(palette)
        Path(target).expanduser().write_text(rendered)

    # reload app
    reload_cmd_file = APPS_DIR / app_name / "app.json"
    if reload_cmd_file.exists():
        try:
            cfg = json.loads(reload_cmd_file.read_text())
            cmd = cfg.get("reload_cmd")
            if cmd:
                if isinstance(cmd, str):
                    cmd = cmd.split()
                run_cmd(cmd)
        except:
            pass

def apply_wallpaper(wallpaper_path):
    if not Path(wallpaper_path).exists():
        print("Wallpaper introuvable:", wallpaper_path)
        return

    subprocess.run([SWWW_BIN, "img", str(wallpaper_path)])

    generate_palette(wallpaper_path)
    temp_file = RICE_DIR / "current_setup.json"
    temp_json = json.loads(temp_file.read_text())
    temp_json["wallpaper"] = str(wallpaper_path)
    temp_file.write_text(json.dumps(temp_json, indent=4))
    for x in temp_json:
        if str(x) != "wallpaper":
            apply_style(str(x), temp_json[x])
    colors = load_palette()
# ----------------------- Main ------------------------
if __name__=="__main__":
    pass
