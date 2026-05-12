#!/usr/bin/env python3
"""Generate an AI Hot Radar poster image with OpenAI Images API.

The script intentionally uses only the Python standard library so the skill can
run in lightweight agent environments.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


API_URL = "https://api.openai.com/v1/images/generations"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AI Hot Radar poster PNG")
    parser.add_argument("--prompt-file", required=True, help="Text file containing the final poster prompt")
    parser.add_argument("--output-dir", required=True, help="Directory for the generated image")
    parser.add_argument("--model", default="gpt-image-1.5", help="OpenAI image model")
    parser.add_argument("--size", default="1024x1536", help="Image size, e.g. 1024x1536")
    parser.add_argument("--quality", default="medium", help="Image quality")
    parser.add_argument("--filename", help="Optional output filename")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY", help="Environment variable that stores the API key")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print the request payload without calling the API")
    return parser.parse_args()


def load_prompt(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Prompt file not found: {path}")
    prompt = path.read_text(encoding="utf-8").strip()
    if not prompt:
        raise SystemExit("Prompt file is empty")
    return prompt


def request_image(api_key: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI Images API failed: HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"OpenAI Images API network error: {exc.reason}") from exc


def save_image(result: dict, output_path: Path) -> None:
    data = result.get("data") or []
    if not data:
        raise SystemExit(f"OpenAI Images API returned no image data: {json.dumps(result, ensure_ascii=False)}")

    first = data[0]
    if first.get("b64_json"):
        output_path.write_bytes(base64.b64decode(first["b64_json"]))
        return

    if first.get("url"):
        with urllib.request.urlopen(first["url"], timeout=180) as response:
            output_path.write_bytes(response.read())
        return

    raise SystemExit(f"OpenAI Images API returned an unsupported image payload: {json.dumps(first, ensure_ascii=False)}")


def main() -> int:
    args = parse_args()
    prompt = load_prompt(Path(args.prompt_file))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = args.filename or f"ai-hot-radar-{timestamp}.png"
    output_path = output_dir / filename

    payload = {
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "quality": args.quality,
        "n": 1,
    }

    if args.dry_run:
        print(json.dumps({"payload": payload, "output_path": str(output_path)}, ensure_ascii=False, indent=2))
        return 0

    api_key = os.environ.get(args.api_key_env, "").strip()
    if not api_key:
        print(
            f"Missing {args.api_key_env}. Set it in Agent Secret or environment before generating poster images.",
            file=sys.stderr,
        )
        return 2

    result = request_image(api_key, payload)
    save_image(result, output_path)
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
