"""Publish an IndexNow key and prepare the URL changes since the live deployment."""
import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


MANIFEST = "indexnow-pages.json"


def read_live_manifest(url):
    request = Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "AxomRank Blog deploy"})
    try:
        with urlopen(request, timeout=15) as response:
            manifest = json.load(response)
            if not isinstance(manifest, dict):
                raise ValueError("live manifest must be a JSON object")
            return manifest
    except HTTPError as error:
        if error.code == 404:  # First deployment on this domain.
            return {}
        raise


def sitemap_hashes(root, base):
    sitemap = ET.parse(root / "sitemap.xml")
    hashes = {}
    for entry in sitemap.findall("./{*}url/{*}loc"):
        url = entry.text
        if not url or not url.startswith(base + "/"):
            raise ValueError(f"Sitemap URL outside {base}: {url}")
        path = root / unquote(urlsplit(url).path.removeprefix(urlsplit(base).path + "/"))
        if path.is_dir():
            path /= "index.html"
        hashes[url] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def prepare(root, base, key):
    if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
        raise ValueError("Invalid IndexNow key")
    base = base.rstrip("/")
    (root / f"{key}.txt").write_text(key, encoding="utf-8")
    current = sitemap_hashes(root, base)
    (root / MANIFEST).write_text(json.dumps(current, sort_keys=True), encoding="utf-8")
    try:
        previous = read_live_manifest(f"{base}/{MANIFEST}")
    except (URLError, TimeoutError, ValueError) as error:
        print(f"IndexNow skipped: unable to read the live manifest ({error})", file=sys.stderr)
        return ""
    changed = sorted(url for url in current.keys() | previous.keys()
                     if url.startswith(base + "/") and current.get(url) != previous.get(url))
    if not changed:
        return ""
    return json.dumps({
        "host": urlsplit(base).hostname, "key": key,
        "keyLocation": f"{base}/{key}.txt", "urlList": changed,
    }, separators=(",", ":"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url")
    parser.add_argument("key")
    parser.add_argument("--root", type=Path, default=Path("_site"))
    args = parser.parse_args()
    print(prepare(args.root, args.base_url, args.key))
