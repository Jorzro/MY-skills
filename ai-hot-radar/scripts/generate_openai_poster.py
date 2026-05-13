#!/usr/bin/env python3
"""Generate an AI Hot Radar poster image with multiple image providers.

Supported providers:
- openai: OpenAI Images API
- minimax: MiniMax image_generation API
- volcengine: Volcengine Ark / Seedream OpenAI-compatible image API
- openrouter: OpenRouter chat/completions image output
- custom: custom OpenAI-compatible /v1/images/generations endpoint

The script uses only the Python standard library so it can run in lightweight
agent environments.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


PROVIDER_DEFAULTS = {
    "openai": {
        "api_url": "https://api.openai.com/v1/images/generations",
        "api_key_envs": ["OPENAI_API_KEY"],
        "model": "gpt-image-1.5",
    },
    "minimax": {
        "api_url": "https://api.minimaxi.com/v1/image_generation",
        "api_key_envs": ["MINIMAX_API_KEY"],
        "model": "image-01",
    },
    "volcengine": {
        "api_url": "https://ark.cn-beijing.volces.com/api/v3/images/generations",
        "api_key_envs": ["ARK_API_KEY", "VOLCENGINE_API_KEY"],
        "model": "doubao-seedream-4-5-251128",
    },
    "openrouter": {
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "api_key_envs": ["OPENROUTER_API_KEY"],
        "model": "google/gemini-3.1-flash-image-preview",
    },
    "custom": {
        "api_url": "",
        "api_key_envs": ["AI_HOT_RADAR_IMAGE_API_KEY"],
        "model": "gpt-image-1.5",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AI Hot Radar poster PNG")
    parser.add_argument("--prompt-file", required=True, help="Text file containing the final poster prompt")
    parser.add_argument("--output-dir", required=True, help="Directory for the generated image")
    parser.add_argument("--provider", default="openai", choices=sorted(PROVIDER_DEFAULTS), help="Image provider")
    parser.add_argument("--model", help="Provider model name")
    parser.add_argument("--size", default="1024x1536", help="Image size, e.g. 1024x1536 or 2K")
    parser.add_argument("--aspect-ratio", default="9:16", help="Aspect ratio for providers that use ratio instead of size")
    parser.add_argument("--quality", default="medium", help="Image quality where supported")
    parser.add_argument("--filename", help="Optional output filename")
    parser.add_argument("--api-url", help="Override provider endpoint URL")
    parser.add_argument("--api-key-env", help="Environment variable that stores the API key")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print the request payload without calling the API")
    return parser.parse_args()


def load_prompt(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Prompt file not found: {path}")
    prompt = path.read_text(encoding="utf-8").strip()
    if not prompt:
        raise SystemExit("Prompt file is empty")
    return prompt


def provider_config(args: argparse.Namespace) -> dict[str, str]:
    defaults = PROVIDER_DEFAULTS[args.provider]
    api_url = args.api_url or os.environ.get("AI_HOT_RADAR_IMAGE_API_URL") or defaults["api_url"]
    if args.provider == "custom" and not api_url:
        raise SystemExit("Provider custom requires --api-url or AI_HOT_RADAR_IMAGE_API_URL")
    envs = [args.api_key_env] if args.api_key_env else defaults["api_key_envs"]
    selected_env = next((name for name in envs if os.environ.get(name, "").strip()), envs[0])
    return {
        "provider": args.provider,
        "api_url": api_url,
        "api_key_env": selected_env,
        "api_key_envs": ",".join(envs),
        "model": args.model or defaults["model"],
    }


def build_payload(args: argparse.Namespace, prompt: str, model: str) -> dict[str, Any]:
    if args.provider in {"openai", "custom"}:
        return {
            "model": model,
            "prompt": prompt,
            "size": args.size,
            "quality": args.quality,
            "n": 1,
        }

    if args.provider == "volcengine":
        return {
            "model": model,
            "prompt": prompt,
            "size": args.size,
            "response_format": "url",
            "watermark": False,
        }

    if args.provider == "minimax":
        return {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": args.aspect_ratio,
            "response_format": "url",
            "n": 1,
            "prompt_optimizer": True,
        }

    if args.provider == "openrouter":
        return {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
            "image_config": {"aspect_ratio": args.aspect_ratio},
            "stream": False,
        }

    raise SystemExit(f"Unsupported provider: {args.provider}")


def post_json(api_url: str, api_key: str, payload: dict[str, Any], provider: str) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://github.com/Jorzro/MY-skills"
        headers["X-Title"] = "AI Hot Radar"

    request = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"{provider} image API failed: HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"{provider} image API network error: {exc.reason}") from exc


def extract_image_refs(result: dict[str, Any]) -> list[str]:
    refs: list[str] = []

    data = result.get("data")
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key in ("b64_json", "url"):
                    value = item.get(key)
                    if isinstance(value, str) and value:
                        refs.append(value)
    elif isinstance(data, dict):
        inner_data = data.get("data")
        if isinstance(inner_data, list):
            for item in inner_data:
                if isinstance(item, dict):
                    for key in ("b64_json", "url"):
                        value = item.get(key)
                        if isinstance(value, str) and value:
                            refs.append(value)
        for key in ("image_urls", "images"):
            value = data.get(key)
            if isinstance(value, list):
                refs.extend(str(item) for item in value if item)

    for key in ("image_urls", "images", "urls"):
        value = result.get(key)
        if isinstance(value, list):
            refs.extend(str(item) for item in value if item)

    for choice in result.get("choices") or []:
        message = choice.get("message") if isinstance(choice, dict) else None
        if not isinstance(message, dict):
            continue
        for image in message.get("images") or []:
            if not isinstance(image, dict):
                continue
            image_url = image.get("image_url") or image.get("imageUrl")
            if isinstance(image_url, dict):
                url = image_url.get("url")
                if isinstance(url, str) and url:
                    refs.append(url)

    return refs


def write_data_url(data_url: str, output_path: Path) -> None:
    match = re.match(r"^data:(?P<mime>[-\w.]+/[-\w.+]+);base64,(?P<data>.+)$", data_url, re.DOTALL)
    if not match:
        raise SystemExit("Unsupported data URL image payload")
    suffix = mimetypes.guess_extension(match.group("mime")) or output_path.suffix
    if suffix and output_path.suffix != suffix:
        output_path = output_path.with_suffix(suffix)
    output_path.write_bytes(base64.b64decode(match.group("data")))
    print(str(output_path))


def save_image(result: dict[str, Any], output_path: Path) -> None:
    refs = extract_image_refs(result)
    if not refs:
        raise SystemExit(f"Image API returned no image data: {json.dumps(result, ensure_ascii=False)[:2000]}")

    first = refs[0]
    if first.startswith("data:image/"):
        write_data_url(first, output_path)
        return

    if first.startswith("http://") or first.startswith("https://"):
        with urllib.request.urlopen(first, timeout=240) as response:
            output_path.write_bytes(response.read())
        print(str(output_path))
        return

    try:
        output_path.write_bytes(base64.b64decode(first))
        print(str(output_path))
    except Exception as exc:  # noqa: BLE001 - keep script dependency-free and explicit.
        raise SystemExit(f"Unsupported image payload: {first[:120]}") from exc


def main() -> int:
    args = parse_args()
    prompt = load_prompt(Path(args.prompt_file))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = args.filename or f"ai-hot-radar-{args.provider}-{timestamp}.png"
    output_path = output_dir / filename

    config = provider_config(args)
    payload = build_payload(args, prompt, config["model"])

    if args.dry_run:
        print(json.dumps({"config": config, "payload": payload, "output_path": str(output_path)}, ensure_ascii=False, indent=2))
        return 0

    api_key = os.environ.get(config["api_key_env"], "").strip()
    if not api_key:
        print(
            f"Missing {config['api_key_envs']}. Set one in Agent Secret or environment before generating poster images.",
            file=sys.stderr,
        )
        return 2

    result = post_json(config["api_url"], api_key, payload, args.provider)
    save_image(result, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
