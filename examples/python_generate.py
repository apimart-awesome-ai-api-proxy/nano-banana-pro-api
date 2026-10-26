#!/usr/bin/env python3
"""Generate one image with Nano Banana Pro (gemini-3-pro-image-preview) and download the result."""

import argparse, os, pathlib, time
import requests

BASE = os.environ.get("APIMART_BASE_URL", "https://api.apimart.ai/v1")
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}


def generate(prompt: str, size: str = "1:1", resolution: str = "1K",
             references: list[str] | None = None) -> dict:
    body = {"model": "gemini-3-pro-image-preview", "prompt": prompt, "size": size, "resolution": resolution, "n": 1}
    if references:
        body["image_urls"] = references
    created = requests.post(f"{BASE}/images/generations", headers=HEADERS, json=body, timeout=60)
    created.raise_for_status()
    task_id = created.json()["data"]["id"]
    delay = 3
    for _ in range(60):
        task = requests.get(f"{BASE}/tasks/{task_id}", headers=HEADERS, timeout=60).json()["data"]
        if task["status"] in ("completed", "failed"):
            return task
        time.sleep(delay)
        delay = min(delay * 2, 10)
    raise TimeoutError(task_id)


def download_images(task: dict, output: pathlib.Path) -> list[pathlib.Path]:
    output.mkdir(parents=True, exist_ok=True)
    saved = []
    for image in task.get("result", {}).get("images", []):
        url = image.get("url")
        if not url:
            continue
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        dest = output / url.rsplit("/", 1)[-1]
        dest.write_bytes(response.content)
        saved.append(dest)
    return saved


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Nano Banana Pro image generation")
    ap.add_argument("--prompt", default="A bamboo forest path under moonlight")
    ap.add_argument("--size", default="1:1", help="`auto`, `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`")
    ap.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"])
    ap.add_argument("--reference", action="append", help="reference image URL or data URL (repeatable)")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    task = generate(args.prompt, args.size, args.resolution, args.reference)
    print(f"status={task['status']} cost={task.get('cost')} credits={task.get('credits_cost')}")
    for dest in download_images(task, pathlib.Path(args.out)):
        print("saved", dest)
