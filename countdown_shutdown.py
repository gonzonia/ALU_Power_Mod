#!/usr/bin/env python3
"""
countdown_shutdown.py

Writes a full-screen countdown message directly to /dev/fb0, reading
pre-rendered frames from disk (see generate_frames.py)

Usage:
    python3 countdown_shutdown.py --seconds 5
    python3 countdown_shutdown.py --seconds 5 --reboot
"""

import argparse
import subprocess
import time
import logging

logging.basicConfig(
    filename="/rcade/share/userscripts/countdown.log",
    filemode="w",
    level=logging.WARNING,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

COUNTDOWN = 5
DEBUG=False
FB_PATH = "/dev/fb0"
FRAMES_DIR = "/rcade/share/userscripts/frames"


def load_frame(name: str) -> bytes:
    path = f"{FRAMES_DIR}/{name}"
    with open(path, "rb") as f:
        return f.read()


def hold_frame(fb, frame_bytes: bytes, duration: float, repaint_interval: float = 0.05):
    """Keep writing the same frame for `duration` seconds to outlast ES's own frames."""
    logging.info("Holding frame for %.1fs", duration)
    end = time.time() + duration
    while time.time() < end:
        fb.seek(0)
        fb.write(frame_bytes)
        fb.flush()
        time.sleep(repaint_interval)


def kill_es():
    logging.info("Killing ES")
    subprocess.Popen(["sh", "-c", "/etc/init.d/S31rcadeboot stop"])


def main():
    logging.info("Parsing arguments")
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=COUNTDOWN)
    parser.add_argument("--skip-kill", action="store_true", help="don't kill ES (for manual testing)")
    parser.add_argument("--reboot", action="store_true", help="reboot message instead of shutdown")
    args = parser.parse_args()

    if not args.skip_kill:
        kill_es()

    prefix = "reboot" if args.reboot else "shutdown"
    cmd = "reboot" if args.reboot else "shutdown -h now"

    labels = [f"{prefix}_{i}.raw" for i in range(args.seconds, 0, -1)] + [f"{prefix}_final.raw"]

    logging.info("Loading pre-rendered frames")
    frames = [load_frame(name) for name in labels]

    with open(FB_PATH, "wb") as fb:
        for name, frame in zip(labels, frames):
            logging.info("Displaying %s", name)
            print(f"[fb] {name}")
            hold_frame(fb, frame, duration=1.0)

    logging.info("Running shutdown/reboot command")
    subprocess.Popen(["sh", "-c", cmd])


if __name__ == "__main__":
    main()
