#!/usr/bin/env python3
"""
generate_frames.py

Run this ONCE (or whenever the message text/font/resolution changes) to
pre-render every countdown frame to raw fb0-format bytes on disk.

Usage:
    python3 generate_frames.py
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FB_PATH = "/dev/fb0"
XRES, YRES = 1920, 1080
FONT_PATH = "/rcade/resources/emulationstation/SourceSansPro-Regular.ttf"
OUT_DIR = "/rcade/share/userscripts/frames"

MAX_SECONDS = 10  # pre-render countdown numbers 1..MAX_SECONDS


def render_frame(lines, font_size=120, line_spacing=20) -> bytes:
    """Render one or more centered lines of text, return raw BGRX bytes for fb0."""
    img = Image.new("RGB", (XRES, YRES), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, font_size)

    if isinstance(lines, str):
        lines = [lines]

    # measure each line
    sizes = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        sizes.append((bbox[2] - bbox[0], bbox[3] - bbox[1], bbox[0], bbox[1]))

    total_h = sum(s[1] for s in sizes) + line_spacing * (len(lines) - 1)
    y = (YRES - total_h) // 2

    for line, (w, h, bx0, by0) in zip(lines, sizes):
        x = (XRES - w) // 2 - bx0
        draw.text((x, y - by0), line, font=font, fill=(255, 255, 255))
        y += h + line_spacing

    arr = np.array(img, dtype=np.uint8)  # R,G,B
    out = np.zeros((YRES, XRES, 4), dtype=np.uint8)
    out[:, :, 0] = arr[:, :, 2]  # B
    out[:, :, 1] = arr[:, :, 1]  # G
    out[:, :, 2] = arr[:, :, 0]  # R
    return out.tobytes()


def save(name: str, data: bytes):
    path = os.path.join(OUT_DIR, name)
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes)")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for i in range(1, MAX_SECONDS + 1):
        save(f"shutdown_{i}.raw", render_frame(f"Shutting down in {i}..."))
        save(f"reboot_{i}.raw", render_frame(f"Rebooting in {i}..."))

    # final messages, split across two lines so they fit the screen width
    save("shutdown_final.raw", render_frame([
        "Please wait while the",
        "system shuts down.",
    ]))
    save("reboot_final.raw", render_frame([
        "Please wait while the",
        "system reboots.",
    ]))


if __name__ == "__main__":
    main()
